void jsonPost() {
  
  power_vector[power_vector_index] = getPower(); // Pega potencia no instante e armazena em um vetor
  power_vector_index++;
  Serial.print("indice power vector: ");
  Serial.println(power_vector_index);

  if(power_vector_index==postsampling)
  {
  
  for(int i=0;i<postsampling;i++)
  {
  power_vectorCopy[i]=power_vector[i];
  }
  post_flag=true;
  }
}


double getPower() {
  //double realPower, apparentPower, powerFactor, Vrms, Irms;

  unsigned int crossings = 20;
  unsigned int timeout = 2000;

  unsigned int crossCount = 0;                             //Used to measure number of times threshold is crossed.
  unsigned int numberOfSamples = 0;                        //This is now incremented

  //-------------------------------------------------------------------------------------------------------------------------
  // 1) Waits for the waveform to be close to 'zero' (mid-scale adc) part in sin curve.
  //-------------------------------------------------------------------------------------------------------------------------
  unsigned long start = millis();    //millis()-start makes sure it doesnt get stuck in the loop if there is an error.

  while (1)                                  //the while loop...
  {
    startV = adc0.readChannel(1);                    //using the voltage waveform
    if ((startV < (ADC_COUNTS * 0.55)) && (startV > (ADC_COUNTS * 0.45))) break; //check its within range
    if ((millis() - start) > timeout) break;

  }

  //-------------------------------------------------------------------------------------------------------------------------
  // 2) Main measurement loop
  //-------------------------------------------------------------------------------------------------------------------------
  start = millis();

  while ((crossCount < crossings) && ((millis() - start) < timeout))
  {

    numberOfSamples++;                       //Count number of times looped.
    lastFilteredV = filteredV;               //Used for delay/phase compensation

    //-----------------------------------------------------------------------------
    // A) Read in raw voltage and current samples
    //-----------------------------------------------------------------------------
    sampleV = adc0.readChannel(1);                 //Read in raw voltage signal
    sampleI = adc0.readChannel(0);                 //Read in raw current signal
    //-----------------------------------------------------------------------------
    // B) Apply digital low pass filters to extract the 2.5 V or 1.65 V dc offset,
    //     then subtract this - signal is now centred on 0 counts.
    //-----------------------------------------------------------------------------
    offsetV = offsetV + ((sampleV - offsetV) / 4096);
    filteredV = sampleV - offsetV;
    offsetI = offsetI + ((sampleI - offsetI) / 4096);
    filteredI = sampleI - offsetI;

    //-----------------------------------------------------------------------------
    // C) Root-mean-square method voltage
    //-----------------------------------------------------------------------------
    sqV = filteredV * filteredV;                //1) square voltage values
    sumV += sqV;                                //2) sum

    //-----------------------------------------------------------------------------
    // D) Root-mean-square method current
    //-----------------------------------------------------------------------------
    sqI = filteredI * filteredI;                //1) square current values
    sumI += sqI;                                //2) sum

    //-----------------------------------------------------------------------------
    // E) Phase calibration
    //-----------------------------------------------------------------------------
    phaseShiftedV = lastFilteredV + PHASECAL * (filteredV - lastFilteredV);

    //-----------------------------------------------------------------------------
    // F) Instantaneous power calc
    //-----------------------------------------------------------------------------
    instP = phaseShiftedV * filteredI;          //Instantaneous Power
    sumP += instP;                              //Sum

    //-----------------------------------------------------------------------------
    // G) Find the number of times the voltage has crossed the initial voltage
    //    - every 2 crosses we will have sampled 1 wavelength
    //    - so this method allows us to sample an integer number of half wavelengths which increases accuracy
    //-----------------------------------------------------------------------------
    lastVCross = checkVCross;
    if (sampleV > startV) checkVCross = true;
    else checkVCross = false;
    if (numberOfSamples == 1) lastVCross = checkVCross;

    if (lastVCross != checkVCross) crossCount++;

  }

  //-------------------------------------------------------------------------------------------------------------------------
  // 3) Post loop calculations
  //-------------------------------------------------------------------------------------------------------------------------
  //Calculation of the root of the mean of the voltage and current squared (rms)
  //Calibration coefficients applied.

  double V_RATIO = VCAL * ((SupplyVoltageV / 1000.0) / (ADC_COUNTS));
  Vrms = V_RATIO * sqrt(sumV / numberOfSamples);

  double I_RATIO = ICAL * ((SupplyVoltageI / 1000.0) / (ADC_COUNTS));
  Irms = I_RATIO * sqrt(sumI / numberOfSamples);

  //Calculation power values
  realPower = V_RATIO * I_RATIO * sumP / numberOfSamples;
  //apparentPower = Vrms * Irms;
  //powerFactor = realPower / apparentPower;

  Serial.print("Vrms: ");
  Serial.print(Vrms);
  Serial.print(" - Irms: ");
  Serial.println(Irms);
  //Serial.println(WiFi.status());

  //Serial.print(" - realPower: ");
  //Serial.print(realPower);
  //Serial.print(" - powerFactor: ");
  //Serial.println(powerFactor);

  //Reset accumulators
  sumV = 0;
  sumI = 0;
  sumP = 0;

  return realPower;
}


void rtcInit() {
  struct tm timeinfo;

  gmtOffset_sec = EEPROM.readInt(90) * 3600;

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer); // Configura servidor NTP para atualizar RTC

  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }

  if (getLocalTime(&timeinfo)) {

    Serial.println("RTC lost power, lets set the time!");


    Serial.println(timeinfo.tm_year + 1900);
    Serial.println(timeinfo.tm_mon + 1);
    Serial.println(timeinfo.tm_mday);
    Serial.println(timeinfo.tm_hour);
    Serial.println(timeinfo.tm_min);
    Serial.println(timeinfo.tm_sec);

    rtc.adjust(DateTime(timeinfo.tm_year + 1900, timeinfo.tm_mon + 1, timeinfo.tm_mday, timeinfo.tm_hour, timeinfo.tm_min, timeinfo.tm_sec));
  }
}
