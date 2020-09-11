#include <WiFi.h>
#include <SPIFFS.h>
#include <MCP3202.h>
#include <EEPROM.h>
#include <NTPClient.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include "time.h"
#include <Wire.h>
#include <WiFiUdp.h>

#define ADC_CS_PIN  16
#define DHT22_PIN   13

#define ADC_BITS    12
#define ADC_COUNTS  (1 << ADC_BITS)
#define ICAL        18.9    //Valor de calibracao para corrente
#define VCAL        271.3   //Valor de calibracao para tensao
#define PHASECAL    1.7     //Valor de calibracao para fase

//Medidor A
//#define ICAL        28.95    //Valor de calibracao para corrente
//#define VCAL        244.8

#define DHTTYPE DHT22

///////////////////////////////Adauto///////////////////////////////////////
#define REDE "Bruna"
#define PASSWORD "Bruna1993"
#define MAX_NAME_FILE 30
#define FAILED_ATTEMPT 30 
int countReset = 0;
////////////////////////////////FIM////////////////////////////////////////

MCP3202 adc0 = MCP3202(ADC_CS_PIN); // Instancia ADC externo com pino CS 16


IPAddress local_IP(192, 168, 4, 1);
IPAddress gateway(192, 168, 4, 9);
IPAddress subnet(255, 255, 255, 0);
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "a.ntp.br", -14400, 100);

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

static uint8_t taskCoreZero = 0;
static uint8_t taskCoreOne  = 1;

TaskHandle_t Task1;
TaskHandle_t Task2;
const short int postsampling = 60; // amostras por post
const short int powerline = 60;

double power_vector[postsampling];
double power_matrix[powerline][postsampling];
unsigned long time_vector[powerline];

byte power_vector_index = 0;

short int k = 0;
short int j = 0;

char payload[2000];


void setup()
{

  WiFi.disconnect(true);
  WiFi.mode(WIFI_STA);
  Serial.begin(115200); // Inicializa monitor serial

  adc0.begin(); // Inicializa ADC externo
  EEPROM.begin(128);  // Inicializa EEPROM

  ///////////////////////////////Adauto///////////////////////////////////////
  // --- Inicializando SPIFSS ---
  if (SPIFFS.begin(true)) {
    Serial.println("Ok");
    loadDataEnergy();
  } else {
    Serial.println("Falha");
  }
  ////////////////////////////////FIM////////////////////////////////////////
  
  while (wifiConfig() == 0) { // Aguarda conexão com rede Wi-Fi
    while (wifi_flag == 0) {  // Se não conseguiu, cria AP para configuração
      Serial.println("Esperando configuração");
      ///////////////////////////////Adauto///////////////////////////////////////
      lookingForNW();
      ////////////////////////////////FIM////////////////////////////////////////
      delay(500);
    }
  }
 
  for (int i = 0; i < 25; i++)
  {
    getPower();
  }
  
  NTPCheck();
  Serial.println("NTP CHECADO");
  ///////////////////////////////Adauto///////////////////////////////////////
  Serial.println(sendLog("Power"));
  Serial.println(sendLog("Com"));
  ////////////////////////////////FIM////////////////////////////////////////
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


void loop() {}


void TaskPower( void * pvParameters ) 
{

  while (true) 
  {
    int timeloop = millis();
    ///////////////////////////////Adauto///////////////////////////////////////
    //recordLog("Power", makeContentPW(), "start:ComputerPower");
    logPW("start:ComputerPower");
    ////////////////////////////////FIM////////////////////////////////////////
    ComputePower();
    ///////////////////////////////Adauto///////////////////////////////////////
    //recordLog("Power", makeContentPW(), "end:ComputerPower");
    logPW("end:ComputerPower");
    ////////////////////////////////FIM////////////////////////////////////////
    timeloop = millis() - timeloop;
    //Serial.print(timeloop);
    //Serial.print(" ");
  
    if (timeloop < 1000)
    {
      delay(1000 - timeloop);
    }
  }
}



void TaskCommunication( void * pvParameters )
{

  while (true)
  {
    if (post_flag == true) {

      while (k < j)
      {

        DataToJson();

        if (WiFi.status() == WL_CONNECTED)
        {
          ///////////////////////////////Adauto///////////////////////////////////////
          //recordLog("Com", makeContentCM(), "start:PostToServer");
          logCM("start:PostToServer");
          ////////////////////////////////FIM////////////////////////////////////////
          PostToServer();
          ///////////////////////////////Adauto///////////////////////////////////////
          //recordLog("Com", makeContentCM(), "end:PostToServer");
          logCM("end:PostToServer");
          ////////////////////////////////FIM////////////////////////////////////////
        }

        if (WiFi.status() != WL_CONNECTED)
        {
          ///////////////////////////////Adauto///////////////////////////////////////
          //recordLog("Com",  makeContentCM(), "start:staReconnect");
          logCM("start:1_nexReconnect");
          
          //staReconnect();
          if(nexReconnect()){
            logCM("sucesso:1_nexReconnect");
          }else{
            logCM("falha:1_nexReconnect");
          }
         
          //recordLog("Com",  makeContentCM(), "end:staReconnect");
          logCM("end:1_nexReconnect");
          ////////////////////////////////FIM////////////////////////////////////////
        }
  
        if (k >= j)
        {
          post_flag = false;
          break;
        }
      }
    }
    delay(100);

  }
}



void NTPCheck()
{
  timeClient.begin();

  while (!timeClient.forceUpdate()) {
    Serial.println("Atualizando NTP");
  }
  Serial.println(timeClient.getFormattedTime());
}

String getTimeStampString(int k) 
{

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
