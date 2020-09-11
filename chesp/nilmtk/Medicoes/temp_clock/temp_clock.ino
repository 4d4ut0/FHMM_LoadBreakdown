#include <Timezone.h>

TimeChangeRule myDST = {"EDT", Second, Sun, Mar, 2, -240};    // Daylight time = UTC - 4 hours
TimeChangeRule mySTD = {"EST", First, Sun, Nov, 2, -300};     // Standard time = UTC - 5 hours
Timezone myTZ(myDST, mySTD);

TimeChangeRule *tcr; 

void setup()

{

 setTime(myTZ.toUTC(compileTime()));
 
 Serial.begin(9600);
  
 analogReference(INTERNAL);

}




void loop()

{ 
  
 time_t utc = now();
 Serial.print(utc);
 Serial.print(" ");
 Serial.println("100");
  

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





