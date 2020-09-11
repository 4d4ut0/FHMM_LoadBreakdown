#include <WiFi.h>
#include <MCP3202.h>
#include <EEPROM.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "time.h"
//#include "soc/soc.h"
//#include "soc/rtc_cntl_reg.h"
#include "RTClib.h"
#include "DHT.h"

#define ADC_CS_PIN  16
#define DHT22_PIN   13
#define LED_PIN     2

#define ADC_BITS    12
#define ADC_COUNTS  (1 << ADC_BITS)
#define ICAL        20.2    //Valor de calibracao para corrente
#define VCAL        258.7   //Valor de calibracao para tensao
#define PHASECAL    1.2     //Valor de calibracao para fase

#define DHTTYPE DHT22

MCP3202 adc0 = MCP3202(ADC_CS_PIN); // Instancia ADC externo com pino CS 16
DHT dht(DHT22_PIN, DHTTYPE);

IPAddress local_IP(192, 168, 4, 1);
IPAddress gateway(192, 168, 4, 9);
IPAddress subnet(255, 255, 255, 0);

RTC_DS3231 rtc;
AsyncWebServer server(80);

/* Varivaeis para a funcao de calcular tensao e corrente, elas precisam ser globais */
int sampleI0 = 0;                      //Armazena amostra raw do ADC
int sampleI1 = 0;                      //Armazena amostra raw do ADC
int sampleV = 0;                      //Armazena amostra raw do ADC
double lastFilteredV, filteredV;      //Filtered_ is the raw analog value minus the DC offset
double filteredI0;
double filteredI1;
double offsetV = ADC_COUNTS >> 1;     //Low-pass filter output
double offsetI0 = ADC_COUNTS >> 1;     //Low-pass filter output
double offsetI1 = ADC_COUNTS >> 1;     //Low-pass filter output
double phaseShiftedV;                 //Holds the calibrated phase shifted voltage.
double sqV, sumV, sqI0, sumI0, instP0, sumP0, instP1, sumP1, sqI1, sumI1; //sq = squared, sum = Sum, inst = instantaneous
int startV;                           //Instantaneous voltage at start of sample window.
boolean lastVCross, checkVCross;      //Used to measure number of times threshold is crossed.
double realPower0, realPower1, apparentPower0,apparentPower1, powerFactor, Vrms, Irms0, Irms1;
int SupplyVoltageV = 3300;
int SupplyVoltageI = 5000;

const short int postsampling = 12;
double power_vector[postsampling];
double power_vectorCopy[postsampling];
byte power_vector_index = 0;

const char* ntpServer = "a.ntp.br";
long  gmtOffset_sec = -10800;
const int   daylightOffset_sec = 0;

boolean wifi_flag = 0;
boolean post_flag = false;

short int iconv = 0;

static volatile uint8_t timer_flag = 0;

TaskHandle_t Task1;
TaskHandle_t Task2;

struct tm timeinfo;

void setup()
{
  Serial.begin(115200); // Inicializa monitor serial

  adc0.begin(); // Inicializa ADC externo
  pinMode(LED_PIN, OUTPUT);

  //dht.begin();  // Inicializa sensor de temperatura DHT22
  EEPROM.begin(128);  // Inicializa EEPROM

  analogReadResolution(12);
  analogSetAttenuation(ADC_0db);

  while (wifiConfig() == 0) { // Aguarda conexão com rede Wi-Fi
    while (wifi_flag == 0) {  // Se não conseguiu, cria AP para configuração
      Serial.write('a');
      delay(500);
    }
  }

  rtcInit();  // Inicializa RTC
  while (true)
  {
    getLocalTime(&timeinfo);
    
    Serial.print("Sincronizando...");
    Serial.println(60 - timeinfo.tm_sec);

    if (timeinfo.tm_sec == 0)
    {
      break;
    }
    delay(300);
  }


  xTaskCreatePinnedToCore(
    TaskPower,   /* Task function. */
    "Task1",     /* name of task. */
    10000,       /* Stack size of task */
    NULL,        /* parameter of the task */
    1,           /* priority of the task */
    &Task1,      /* Task handle to keep track of created task */
    0);          /* pin task to core 0 */
  delay(500);

  //create a task that will be executed in the Task2code() function, with priority 1 and executed on core 1
  xTaskCreatePinnedToCore(
    TaskCommunication,   /* Task function. */
    "Task2",     /* name of task. */
    10000,       /* Stack size of task */
    NULL,        /* parameter of the task */
    1,           /* priority of the task */
    &Task2,      /* Task handle to keep track of created task */
    1);          /* pin task to core 1 */
  delay(500);

}

void loop()
{ 
}

void TaskPower( void * pvParameters ) {

  for (;;) {
    Serial.println("Core 0 - GetPower");

    if (getLocalTime(&timeinfo)) {
      if ((timeinfo.tm_sec % 5) == 0 && power_vector_index < postsampling) {
        jsonPost();
      }
    }

    delay(1000);

  }


}

void TaskCommunication( void * pvParameters ) {

  for (;;) {
    Serial.println("Core 1 - Comunicação");


    if (power_vector_index >= postsampling) { // Se pegou 6 amostras de potencia
      post_flag = false;
      power_vector_index = 0;
      wifiConfig();
      delay(5000);
      iconv++;


      char timestamp[32];
      char payload[512];
      StaticJsonDocument<512> doc; // Cria JSON

      /* Le temperatura e umidade */
      float humidity = dht.readHumidity();
      float temperature = dht.readTemperature();

      /* Se a leitura de temperatura e umidade falhar, recebe zero */
      if (isnan(humidity) || isnan(temperature)) {
        humidity = 0;
        temperature = 0;
      }

      /* Cria timestamp */
      strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%S.000z", &timeinfo);

      /* Adiciona variaveis no JSON */
      doc["Id"] = WiFi.macAddress();
      doc["DataRegistro"] = timestamp;

      JsonArray data = doc.createNestedArray("Potencias");


      if (iconv > 2)
      {
        iconv = 3;
        for (int i = 0; i < postsampling; i++) {
          data.add(power_vectorCopy[i]);
        }
      }

      else {
        for (int i = 0; i < postsampling; i++) {
          data.add(0);
        }
      }

      doc["Potencia"] = 0;
      doc["Temperatura"] = temperature;
      doc["Umidade"] = humidity;

      serializeJson(doc, payload);  // Converte JSON para vetor de char
      Serial.println(payload);

      //boolean onwifi = wifiConfig();
      //delay(5000);

      if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

        HTTPClient http;
        http.begin("http://nexsolar.sytes.net/ceb/api/consumo");  //Specify destination for HTTP request
        http.addHeader("Content-Type", "application/json");             //Specify content-type header

        int httpResponseCode = http.POST(payload);   //Send the actual POST request

        if (httpResponseCode > 0) {

          String response = http.getString();                       //Get the response to the request

          Serial.println(httpResponseCode);   //Print return code
          Serial.println(response);           //Print request answer

        } else {

          Serial.print("Error on sending POST: ");
          Serial.println(httpResponseCode);
        }

        http.end();  //Free resources

      }
    }

    delay(1000);
  }

}
