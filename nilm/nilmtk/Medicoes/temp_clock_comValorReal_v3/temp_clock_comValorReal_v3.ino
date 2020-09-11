#include <Timezone.h>
#include "EmonLib.h"             // Include Emon Library

TimeChangeRule myDST = {"EDT", Second, Sun, Mar, 2, -240};    // Daylight time = UTC - 4 hours
TimeChangeRule mySTD = {"EST", First, Sun, Nov, 2, -300};     // Standard time = UTC - 5 hours
Timezone myTZ(myDST, mySTD);

TimeChangeRule *tcr; 
EnergyMonitor emon1;             // Create an instance


void setup()

{

 setTime(myTZ.toUTC(compileTime()));
 
 Serial.begin(9600);
  
 //analogReference(INTERNAL);

 /* DE FABRICA*/
  emon1.voltage(2, 160, 1.7);  // Voltage: input pin, calibration, phase_shift
  emon1.currentIT(0, 57.1);       // Current: input pin, calibration.
  //resistor azul 2,2k
  emon1.currentTXI1(1, 3.9);
  //resistor normal 2,2k
  emon1.currentTXI2(3, 17.9);

}




void loop()

{ 
  
 time_t utc = now();
 
 //Serial.println("100");
 
  emon1.calcVI(20, 2000);        // Calculate all. No.of half wavelengths (crossings), time-out
  emon1.serialprint();           // Print out all variables (realpower, apparent power, Vrms, Irms, power factor)

  //TOTAL:
  float realPower       = emon1.realPower;        //extract Real Power into variable
  float apparentPower   = emon1.apparentPower;    //extract Apparent Power into variable
  float powerFActor     = emon1.powerFactor;      //extract Power Factor into Variable
  float supplyVoltage   = emon1.Vrms;             //extract Vrms into Variable
  float Irms            = emon1.Irms;             //extract Irms into Variable
  float PotReativa      = emon1.PotReativa;             //extract Irms into Variable 

  //CN:1:
  float realPower1       = emon1.realPower1;        //extract Real Power into variable
  float apparentPower1   = emon1.apparentPower1;    //extract Apparent Power into variable
  float powerFActor1     = emon1.powerFactor1;      //extract Power Factor into Variable
  float Irms1            = emon1.Irms1;             //extract Irms into Variable
  float PotReativa1      = emon1.PotReativa1;             //extract Irms into Variable 

//CN:2:
  float realPower2       = emon1.realPower2;        //extract Real Power into variable
  float apparentPower2   = emon1.apparentPower2;    //extract Apparent Power into variable
  float powerFActor2     = emon1.powerFactor2;      //extract Power Factor into Variable
  float Irms2            = emon1.Irms2;             //extract Irms into Variable
  float PotReativa2      = emon1.PotReativa2;             //extract Irms into Variable 


  
 //TOTAL:
  Serial.print(utc);
  Serial.print(" ");
  if (realPower<10)                                                                           Serial.print("00000");
  if (realPower<100 && realPower>10)                                                          Serial.print("0000");
  if (realPower<1000 && realPower>10 && realPower>100)                                        Serial.print("000");
  if (realPower<10000 && realPower>10 && realPower>100 && realPower>1000 )                    Serial.print("00");
  if (realPower<100000 && realPower>10 && realPower>100 && realPower>1000 && realPower>10000) Serial.print("0");
  Serial.print(realPower);
  Serial.print(" ");
  if (apparentPower<10)                                                                                         Serial.print("00000");
  if (apparentPower<100 && apparentPower>10)                                                                    Serial.print("0000");
  if (apparentPower<1000 && apparentPower>10 && apparentPower>100)                                              Serial.print("000");
  if (apparentPower<10000 && apparentPower>10 && apparentPower>100 && apparentPower>1000 )                       Serial.print("00");
  if (apparentPower<100000 && apparentPower>10 && apparentPower>100 && apparentPower>1000 && apparentPower>10000) Serial.print("0");
  Serial.print(apparentPower);
  Serial.print(" ");
  //Serial.print(PotReativa);
  //Serial.print(" ");
  if (supplyVoltage<10)                                                                           Serial.print("00000");
  if (supplyVoltage<100 && supplyVoltage>10)                                                          Serial.print("0000");
  if (supplyVoltage<1000 && supplyVoltage>10 && supplyVoltage>100)                                        Serial.print("000");
  if (supplyVoltage<10000 && supplyVoltage>10 && supplyVoltage>100 && supplyVoltage>1000 )                    Serial.print("00");
  if (supplyVoltage<100000 && supplyVoltage>10 && supplyVoltage>100 && supplyVoltage>1000 && supplyVoltage>10000) Serial.print("0");
  Serial.print(supplyVoltage);
  Serial.print(" ");
  //Serial.print(Irms);
  //Serial.print(" ");
  
  //CN:1:
  /* real power está errado!*/
  //Serial.print(realPower1);
  //Serial.print(" ");
  if (apparentPower1<10)                                                                           Serial.print("00000");
  if (apparentPower1<100 && apparentPower1>10)                                                          Serial.print("0000");
  if (apparentPower1<1000 && apparentPower1>10 && apparentPower1>100)                                        Serial.print("000");
  if (apparentPower1<10000 && apparentPower1>10 && apparentPower1>100 && apparentPower1>1000 )                    Serial.print("00");
  if (apparentPower1<100000 && apparentPower1>10 && apparentPower1>100 && apparentPower1>1000 && apparentPower1>10000) Serial.print("0");
  Serial.print(apparentPower1);
  Serial.print(" ");
  //Serial.print(PotReativa1);
  //Serial.print(" ");
  //Serial.print(Irms1);
  //Serial.print(" ");
 

 
  //CN:1:
  /* real power está errado!*/
  //Serial.print(realPower1);
  //Serial.print(" ");
  if (apparentPower2<10)                                                                           Serial.print("00000");
  if (apparentPower2<100 && apparentPower2>10)                                                          Serial.print("0000");
  if (apparentPower2<1000 && apparentPower2>10 && apparentPower2>100)                                        Serial.print("000");
  if (apparentPower2<10000 && apparentPower2>10 && apparentPower2>100 && apparentPower2>1000 )                    Serial.print("00");
  if (apparentPower2<100000 && apparentPower2>10 && apparentPower2>100 && apparentPower2>1000 && apparentPower2>10000) Serial.print("0");
  Serial.print(apparentPower2);
  Serial.println(" ");
  //Serial.print(PotReativa2);
  //Serial.print(" ");
 // Serial.print(Irms2);
 // Serial.println(" ");

  

 if (Serial.available())
 
 {

  Serial.read();
  
 }

 
 
 delay(1000);

}


// Function to return the compile date and time as a time_t value
time_t compileTime()
{
    const time_t FUDGE(10);     // fudge factor to allow for compile time (seconds, YMMV)
    const char *compDate = __DATE__, *compTime = __TIME__, *months = "JanFebMarAprMayJunJulAugSepOctNovDec";
    char chMon[3], *m;
    tmElements_t tm;

    strncpy(chMon, compDate, 3);
    chMon[3] = '\0';
    m = strstr(months, chMon);
    tm.Month = ((m - months) / 3 + 1);

    tm.Day = atoi(compDate + 4);
    tm.Year = atoi(compDate + 7) - 1970;
    tm.Hour = atoi(compTime);
    tm.Minute = atoi(compTime + 3);
    tm.Second = atoi(compTime + 6);
    time_t t = makeTime(tm);
    return t + FUDGE;           // add fudge factor to allow for compile time
}





