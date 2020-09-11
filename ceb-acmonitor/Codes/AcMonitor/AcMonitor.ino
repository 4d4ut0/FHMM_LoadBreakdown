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

double power_vector[6];
byte power_vector_index = 0;

const char* ntpServer = "a.ntp.br";
long  gmtOffset_sec = -10800;
const int   daylightOffset_sec = 0;

boolean wifi_flag = 0;

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
}

void loop()
{
  DateTime now = rtc.now(); // Recebe informação de data e hora do RTC

  /* A cada 10 segundos, le potencia */
  if ((now.second() % 5) == 0) {
    jsonPost();
  }
  delay(1000);
}
