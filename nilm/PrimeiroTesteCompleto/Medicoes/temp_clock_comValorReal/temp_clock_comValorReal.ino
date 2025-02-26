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
  emon1.voltage(2, 170, 1.7);  // Voltage: input pin, calibration, phase_shift
  emon1.currentIT(0, 141.1);       // Current: input pin, calibration.
  emon1.currentTXI1(1, 141.1);
  emon1.currentTXI2(3, 141.1);
  emon1.currentTXI3(4, 141.1);
}




void loop()

{ 
  
 time_t utc = now();
 
 //Serial.println("100");
 
  emon1.calcVI(20, 2000);        // Calculate all. No.of half wavelengths (crossings), time-out
  emon1.serialprint();           // Print out all variables (realpower, apparent power, Vrms, Irms, power factor)

  float realPower       = emon1.realPower;        //extract Real Power into variable
  float apparentPower   = emon1.apparentPower;    //extract Apparent Power into variable
  float powerFActor     = emon1.powerFactor;      //extract Power Factor into Variable
  float supplyVoltage   = emon1.Vrms;             //extract Vrms into Variable
  float Irms            = emon1.Irms;             //extract Irms into Variable
  float PotReativa      = emon1.PotReativa;             //extract Irms into Variable 

  Serial.print(utc);
  Serial.print(" ");
  Serial.print(realPower);
  Serial.print(" ");
  Serial.print(apparentPower);
  Serial.print(" ");
  Serial.println(supplyVoltage);

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





