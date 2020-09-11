#include <WiFi.h>
#include <MCP3202.h>
#include <EEPROM.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "time.h"
#include "RTClib.h"
#include "DHT.h"

#define ADC_CS_PIN  16
#define DHT22_PIN   13

#define ADC_BITS    12
#define ADC_COUNTS  (1 << ADC_BITS)
#define ICAL        28.95    //Valor de calibracao para corrente
#define VCAL        244.8   //Valor de calibracao para tensao
#define PHASECAL    1.7     //Valor de calibracao para fase

#define DHTTYPE DHT22

MCP3202 adc0 = MCP3202(ADC_CS_PIN); // Instancia ADC externo com pino CS 16
DHT dht(DHT22_PIN, DHTTYPE);

IPAddress local_IP(192, 168, 4, 1);
IPAddress gateway(192, 168, 4, 9);
IPAddress subnet(255, 255, 255, 0);

RTC_DS3231 rtc;
AsyncWebServer server(80);

/* Varivaeis para a funcao de calcular tensao e corrente, elas precisam ser globais */
int sampleI = 0;                      //Armazena amostra raw do ADC
int sampleV = 0;                      //Armazena amostra raw do ADC
double lastFilteredV, filteredV;      //Filtered_ is the raw analog value minus the DC offset
double filteredI;
double offsetV = ADC_COUNTS >> 1;     //Low-pass filter output
double offsetI = ADC_COUNTS >> 1;     //Low-pass filter output
double phaseShiftedV;                 //Holds the calibrated phase shifted voltage.
double sqV, sumV, sqI, sumI, instP, sumP; //sq = squared, sum = Sum, inst = instantaneous
int startV;                           //Instantaneous voltage at start of sample window.
boolean lastVCross, checkVCross;      //Used to measure number of times threshold is crossed.
double realPower, apparentPower, powerFactor, Vrms, Irms;
int SupplyVoltageV = 3300;
int SupplyVoltageI = 5000;

double power_vector[12];
double power_vectorCopy[12];

byte power_vector_index = 0;

const char* ntpServer = "a.ntp.br";
long  gmtOffset_sec = -10800;
const int   daylightOffset_sec = 0;

boolean wifi_flag = 0;
boolean post_flag = false;

short int iconv = 0;
static uint8_t taskCoreZero = 0;
static uint8_t taskCoreOne  = 1;

TaskHandle_t Task1;
TaskHandle_t Task2;
short int postsampling =12;  // amostras por post

void setup()
{
  Serial.begin(115200); // Inicializa monitor serial

  adc0.begin(); // Inicializa ADC externo
  dht.begin();  // Inicializa sensor de temperatura DHT22
  EEPROM.begin(128);  // Inicializa EEPROM

  while (wifiConfig() == 0) { // Aguarda conexão com rede Wi-Fi
    while (wifi_flag == 0) {  // Se não conseguiu, cria AP para configuração
      Serial.write('a');
      delay(500);
    }
  }  

rtcInit();  // Inicializa RTC
DateTime now = rtc.now();
while(true)
{
DateTime now = rtc.now();
Serial.print("Sincronizando...");
Serial.println(60-now.second());

if(now.second()==0)
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
{}

void TaskPower( void * pvParameters ) {

  for (;;) {
    Serial.println("Core 0 - GetPower");
    DateTime now = rtc.now(); // Recebe informação de data e hora do RTC

    /* A cada 10 segundos, le potencia */
    if ((now.second() % 5) == 0 && power_vector_index<postsampling) {
      jsonPost();
    }
    
    delay(1000);
    
  }

  
}

void TaskCommunication( void * pvParameters ) {

for (;;) {
  Serial.println("Core 1 - Comunicação");
  

  if (power_vector_index >= postsampling) { // Se pegou 6 amostras de potencia
    post_flag=false;
    power_vector_index = 0;
    wifiConfig();
    delay(5000);
    iconv++;


    char timestamp[32];
    char payload[512];
    DateTime now = rtc.now();
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
    sprintf(timestamp, "%04d-%02d-%02dT%02d:%02d:%02d.000Z", now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second());

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
