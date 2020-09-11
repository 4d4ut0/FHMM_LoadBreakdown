void ComputePower() 
{
  power_vector[power_vector_index] = getPower(); // Pega potencia no instante e armazena em um vetor
  power_vector_index++;

  if (power_vector_index == postsampling)
  {

    if (k == j)
    {
      k = 0;
      j = 0;
    }
    
    if((WiFi.status() == WL_CONNECTED))
    {
    timeClient.forceUpdate();
    }
    else{
    timeClient.update();  
    }

    for (int i = 0; i < postsampling; i++)
    {
      if (j >= powerline)
      {
        j = j - 1;
      }
      power_matrix[j][i] = power_vector[i];
    }
    time_vector[j] = timeClient.getEpochTime();
    Serial.println("Armazenado na matriz");
    
    Serial.print("Tempo j: ");
    Serial.println(timeClient.getFormattedTime());
    Serial.print("k: ");
    Serial.print(k);
    Serial.print(" - j: ");
    Serial.println(j);
    
    power_vector_index = 0;
    j++;
    post_flag = true;
  }
  
}

double getPower() {
  double powerSum;

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
    sampleV = analogRead(32);                 //Read in raw voltage signal
    sampleI0 = adc0.readChannel(0);                 //Read in raw current signal
    sampleI1 = adc0.readChannel(1);
    //-----------------------------------------------------------------------------
    // B) Apply digital low pass filters to extract the 2.5 V or 1.65 V dc offset,
    //     then subtract this - signal is now centred on 0 counts.
    //-----------------------------------------------------------------------------
    offsetV = offsetV + ((sampleV - offsetV) / 4096);
    filteredV = sampleV - offsetV;
    offsetI0 = offsetI0 + ((sampleI0 - offsetI0) / 4096);
    filteredI0 = sampleI0 - offsetI0;
    offsetI1 = offsetI1 + ((sampleI1 - offsetI1) / 4096);
    filteredI1 = sampleI1 - offsetI1;

    //-----------------------------------------------------------------------------
    // C) Root-mean-square method voltage
    //-----------------------------------------------------------------------------
    sqV = filteredV * filteredV;                //1) square voltage values
    sumV += sqV;                                //2) sum

    //-----------------------------------------------------------------------------
    // D) Root-mean-square method current
    //-----------------------------------------------------------------------------
    sqI0 = filteredI0 * filteredI0;                //1) square current values
    sumI0 += sqI0;                                //2) sum

    sqI1 = filteredI1 * filteredI1;                //1) square current values
    sumI1 += sqI1;                                //2) sum

    //-----------------------------------------------------------------------------
    // E) Phase calibration
    //-----------------------------------------------------------------------------
    phaseShiftedV = lastFilteredV + PHASECAL * (filteredV - lastFilteredV);

    //-----------------------------------------------------------------------------
    // F) Instantaneous power calc
    //-----------------------------------------------------------------------------
    instP0 = phaseShiftedV * filteredI0;          //Instantaneous Power
    sumP0 += instP0;                              //Sum

    instP1 = phaseShiftedV * filteredI1;          //Instantaneous Power
    sumP1 += instP1;                              //Sum

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

  double I_RATIO0 = ICAL * ((SupplyVoltageI / 1000.0) / (ADC_COUNTS));
  Irms0 = I_RATIO0 * sqrt(sumI0 / numberOfSamples);

  double I_RATIO1 = ICAL * ((SupplyVoltageI / 1000.0) / (ADC_COUNTS));
  Irms1 = I_RATIO1 * sqrt(sumI1 / numberOfSamples);

  //Calculation power values
  realPower0 = V_RATIO * I_RATIO0 * sumP0 / numberOfSamples;
  realPower1 = V_RATIO * I_RATIO1 * sumP1 / numberOfSamples;
  apparentPower0 = Vrms * Irms0;
  apparentPower1 = Vrms * Irms1;
  //powerFactor = realPower / apparentPower;

  powerSum = (abs(realPower0) + abs(realPower1));
  //powerSum = (abs(apparentPower0) + abs(apparentPower1));
    //powerSum = abs(realPower0);

  //Reset accumulators
  sumV = 0;
  sumI0 = 0;
  sumI1 = 0;
  sumP0 = 0;
  sumP1 = 0;

  return powerSum;
}
