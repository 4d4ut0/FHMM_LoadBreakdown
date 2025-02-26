void jsonPost() {
  power_vector[power_vector_index] = getPower(); // Pega potencia no instante e armazena em um vetor
  power_vector_index++;

  Serial.println(power_vector_index);

  //digitalWrite(LED_PIN, HIGH);
  //delay(500);
  //digitalWrite(LED_PIN, LOW);

  if (power_vector_index == 6) { // Se pegou 6 amostras de potencia
    char timestamp[32];
    char payload[512];
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
    //getLocalTime(&timeinfo);

    strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%S.000z", &timeinfo);
    //sprintf(timestamp, "%04d-%02d-%02dT%02d:%02d:%02d.000Z", now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second());

    /* Adiciona variaveis no JSON */
    doc["Id"] = WiFi.macAddress();
    doc["DataRegistro"] = timestamp;

    JsonArray data = doc.createNestedArray("Potencias");

    for (int i = 0; i < 6; i++) {
      data.add(power_vector[i]);
    }

    doc["Potencia"] = 0;
    doc["Temperatura"] = temperature;
    doc["Umidade"] = humidity;

    serializeJson(doc, payload);  // Converte JSON para vetor de char
    Serial.println(payload);
    power_vector_index = 0;

    if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

      HTTPClient http;
      http.begin("http://nexsolar.sytes.net/ceb/api/consumo");  //Specify destination for HTTP request
      http.addHeader("Content-Type", "application/json");             //Specify content-type header

      int httpResponseCode = http.POST(payload);   //Send the actual POST request

      if (httpResponseCode > 0) {

        String response = http.getString();                       //Get the response to the request

        Serial.println(httpResponseCode);   //Print return code
        Serial.println(response);           //Print request answer

      } else {

        Serial.print("Error on sending POST: ");
        Serial.println(httpResponseCode);
      }

      http.end();  //Free resources

    } else {
      Serial.println("Error in WiFi connection");
      ESP.restart();
    }
    //Serial.println(millis());
  }
}

double getPower() {
  double powerAverage;

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
  //apparentPower = Vrms * Irms0;
  //powerFactor = realPower / apparentPower;

  /*Serial.print("Vrms: ");
    Serial.print(Vrms);
    Serial.print(" - Irms0: ");
    Serial.print(Irms0);
    Serial.print(" - Irms1: ");
    Serial.print(Irms1);
    Serial.print(" - realPower0: ");
    Serial.print(realPower0);
    Serial.print(" - realPower1: ");
    Serial.print(realPower1);
    Serial.print(" - powerFactor: ");
    Serial.print(powerFactor);*/

  powerAverage = (abs(realPower0) + abs(realPower1)) * 0.5;

  //Serial.print(" - media: ");
  //Serial.println(media);

  //Reset accumulators
  sumV = 0;
  sumI0 = 0;
  sumI1 = 0;
  sumP0 = 0;
  sumP1 = 0;

  return powerAverage;
}

void rtcInit() {
  struct tm timeinfo;

  gmtOffset_sec = EEPROM.readInt(90) * 3600;

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer); // Configura servidor NTP para atualizar RTC

  /*if (!rtc.begin()) {
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
    }*/
}
