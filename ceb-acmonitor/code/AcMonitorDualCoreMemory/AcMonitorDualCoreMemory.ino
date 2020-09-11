#include <WiFi.h>
#include <MCP3202.h>
#include <EEPROM.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "time.h"
#include <Wire.h>
#include <RtcDS3231.h>
#include "DHT.h"
#include <NTPClient.h>
#include <WiFiUdp.h>
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

RtcDS3231<TwoWire> rtc(Wire);
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

const char* ntpServer = "a.ntp.br";
long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 0;

boolean wifi_flag = 0;
boolean post_flag = false;

short int iconv = 0;
static uint8_t taskCoreZero = 0;
static uint8_t taskCoreOne  = 1;

TaskHandle_t Task1;
TaskHandle_t Task2;
const short int postsampling = 12; // amostras por post
const short int powerline = 800;

double power_vector[postsampling];
double power_matrix[powerline][postsampling];
unsigned long time_vector[powerline];

byte power_vector_index = 0;

short int k = 0;
short int j = 0;

char payload[512];
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "a.ntp.br", 0, 1000);
RtcDateTime now;


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
  delay(2000);
  initRTC();  // Inicializa RTC

  for(int i=0;i<30;i++)
  {
  getPower();
  }
  
  while (true)
  {
    now = rtc.GetDateTime();
    Serial.print("Sincronizando...");
    Serial.println(60 - now.Second());

    if (now.Second() == 0)
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
    //Serial.println("Core 0 - GetPower");
    now = rtc.GetDateTime();
    /* A cada 5 segundos, le potencia */
    if ((now.Second() % 5) == 0 && power_vector_index < postsampling) {
      ComputePower();
    }

    delay(1000);
    
  }

}


void TaskCommunication( void * pvParameters ) {

  for (;;) {
    //Serial.println("Core 1 - Comunicação");

    if (post_flag == true) {
      power_vector_index = 0;
      iconv++;

      for (int i = 0; i < postsampling; i++)
      {

        if (iconv > 2)
        {
          iconv = 3;
        }

        else {
          power_matrix[j][i] = 0;
        }

      }


      while (k < j)
      {
        Serial.print("k: ");
        Serial.println(k);
        Serial.print("j: ");
        Serial.println(j);

        DataToJson();

        if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

          HTTPClient http;
          http.begin("http://nexsolar.sytes.net/ceb/api/consumo");  //Specify destination for HTTP request
          http.addHeader("Content-Type", "application/json");             //Specify content-type header

          int httpResponseCode = http.POST(payload);   //Send the actual POST request
          Serial.println(payload);

          if (httpResponseCode > 0) {

            String response = http.getString();                       //Get the response to the request

            Serial.println(httpResponseCode);   //Print return code
            Serial.println(response);           //Print request answer
            k++;
          }

          else
          {
            Serial.print("Error on sending POST: ");
            Serial.println(httpResponseCode);
            wifiConfig();
          }

          http.end();  //Free resources

        }

        if (WiFi.status() != WL_CONNECTED)
        {
          wifiConfig();
        }

        if (k >= j)
        {
          post_flag = false;
          break;
        }


      }

      if (j == powerline - 1)
      {
        j = powerline - 1;
      }

    }
    delay(1000);
  }

}

void DataToJson()
{
  //char timestamp[32];

  //DateTime now = rtc.now();
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
  //sprintf(timestamp, "%04d-%02d-%02dT%02d:%02d:%02d.000Z", now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second());

  /* Adiciona variaveis no JSON */
  doc["Id"] = WiFi.macAddress();
  doc["DataRegistro"] = getTimeStampString(k);

  JsonArray data = doc.createNestedArray("Potencias");

  for (int i = 0; i < postsampling; i++) {
    data.add(power_matrix[k][i]);
  }

  doc["Potencia"] = 0;
  doc["Temperatura"] = temperature;
  doc["Umidade"] = humidity;

  serializeJson(doc, payload);  // Converte JSON para vetor de char
}


String getTimeStampString(int k) {

  //RtcDateTime now = Rtc.GetDateTime();
  time_t rawtime = time_vector[k];
  struct tm * ti;
  ti = localtime (&rawtime);

  uint16_t year = ti->tm_year + 1900;
  String yearStr = String(year);

  uint8_t month = ti->tm_mon + 1;
  String monthStr = month < 10 ? "0" + String(month) : String(month);

  uint8_t day = ti->tm_mday;
  String dayStr = day < 10 ? "0" + String(day) : String(day);

  uint8_t hours = ti->tm_hour;
  String hoursStr = hours < 10 ? "0" + String(hours) : String(hours);

  uint8_t minutes = ti->tm_min;
  String minuteStr = minutes < 10 ? "0" + String(minutes) : String(minutes);

  uint8_t seconds = ti->tm_sec;
  String secondStr = seconds < 10 ? "0" + String(seconds) : String(seconds);

  return yearStr + "-" + monthStr + "-" + dayStr + " " +
         hoursStr + ":" + minuteStr + ":" + secondStr;
}
