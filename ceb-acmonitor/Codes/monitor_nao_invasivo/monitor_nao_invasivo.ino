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
//#include "RTClib.h"
#include "DHT.h"

#define ADC_CS_PIN  16
#define DHT22_PIN   13
#define LED_PIN     2

#define ADC_BITS    12
#define ADC_COUNTS  (1 << ADC_BITS)
#define ICAL        20.2    //Valor de calibracao para corrente
#define VCAL        258.7   //Valor de calibracao para tensao
#define PHASECAL    3     //Valor de calibracao para fase

#define DHTTYPE DHT22

MCP3202 adc0 = MCP3202(ADC_CS_PIN); // Instancia ADC externo com pino CS 16
DHT dht(DHT22_PIN, DHTTYPE);

IPAddress local_IP(192, 168, 4, 1);
IPAddress gateway(192, 168, 4, 9);
IPAddress subnet(255, 255, 255, 0);

//RTC_DS3231 rtc;
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
double realPower0, realPower1, apparentPower, powerFactor, Vrms, Irms0, Irms1;
int SupplyVoltageV = 3300;
int SupplyVoltageI = 5000;

double power_vector[6];
byte power_vector_index = 0;

const char* ntpServer = "a.ntp.br";
long  gmtOffset_sec = -10800;
const int   daylightOffset_sec = 0;

boolean wifi_flag = 0;

static volatile uint8_t timer_flag = 0;

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
      digitalWrite(LED_PIN, HIGH);
      delay(250);
      digitalWrite(LED_PIN, LOW);
      delay(250);
    }
  }

  rtcInit();  // Inicializa RTC
}

void loop()
{
  if (getLocalTime(&timeinfo)) {
    if ((timeinfo.tm_sec % 10) == 0) {
      jsonPost();
    }
  }
  delay(1000);
}
