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
  emon1.currentIT(0, 165.1);       // Current: input pin, calibration.
  emon1.currentTXI1(1, 165.1);
  emon1.currentTXI2(3, 165.1);
  emon1.currentTXI3(4, 165.1);
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

  //CN:3:
  float realPower3       = emon1.realPower3;        //extract Real Power into variable
  float apparentPower3   = emon1.apparentPower3;    //extract Apparent Power into variable
  float powerFActor3     = emon1.powerFactor3;      //extract Power Factor into Variable
  float Irms3            = emon1.Irms3;             //extract Irms into Variable
  float PotReativa3      = emon1.PotReativa3;             //extract Irms into Variable 

  
 //TOTAL:
  Serial.print(utc);
  Serial.print(" ");
  Serial.print(realPower);
  Serial.print(" ");
  Serial.print(apparentPower);
  Serial.print(" ");
  Serial.print(PotReativa);
  Serial.print(" ");
  Serial.print(supplyVoltage);
  Serial.print(" ");
  Serial.print(Irms);
  Serial.print(" ");
  
  //CN:1:
  /* real power está errado!*/
  //Serial.print(realPower1);
  //Serial.print(" ");
  Serial.print(apparentPower1);
  Serial.print(" ");
  Serial.print(PotReativa1);
  Serial.print(" ");
  Serial.print(Irms1);
  Serial.print(" ");
 

 
  //CN:2:

  Serial.print(apparentPower2);
  Serial.print(" ");
  Serial.print(Irms2);
  Serial.print(" ");

  //CN:3:
  Serial.print(apparentPower3);
  Serial.print(" ");
  Serial.print(Irms3);
  Serial.println(" ");

  

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





