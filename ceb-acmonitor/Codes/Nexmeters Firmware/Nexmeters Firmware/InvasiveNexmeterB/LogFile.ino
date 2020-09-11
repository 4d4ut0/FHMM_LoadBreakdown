// --- Lendo arquivo ---

int sendLog(const char *fileName){
  char fullFileName[MAX_NAME_FILE];
  sprintf(fullFileName,"/Log/%s.txt",fileName);
  File file = SPIFFS.open(fullFileName, "r");
  if (file) {
    DynamicJsonDocument jsonLog(120); // Cria JSON  
    jsonLog["idHardware"] = file.readStringUntil('\n');
    jsonLog["dataRegistro"] = file.readStringUntil('\n');
    jsonLog["evento"] = file.readStringUntil('\n');
    jsonLog["snap"] = file.readStringUntil('\n');
    file.close();
    char dataLog[120];
    serializeJson(jsonLog, dataLog);

    Serial.println(dataLog);

    //enviar arquivo
    HTTPClient http;
    http.begin("http://nexsolar.sytes.net/chesp/api/log/");
    http.addHeader("Content-Type", "application/json");             //Specify content-type header
    int httpResponseCode = http.POST(dataLog);   //Send the actual POST request
    return httpResponseCode;
  }
  return -1;
}

// --- Gravando arquivo ---
void recordLog(const char *fileName, const char *fileContend, const char *flag){
    char fullFileName[MAX_NAME_FILE];
    sprintf(fullFileName,"/Log/%s.txt",fileName);
    File file = SPIFFS.open(fullFileName, "w");
    Serial.println(fileContend);
    if (file) {
      //salvando mac => idEstacao
      String auxLine = WiFi.macAddress();
      auxLine.replace(":", "");
      char line[20];
      strcpy(line, auxLine.c_str());
      file.printf("%s\n",line);
      
      //salvando tempo => dataRegistro
      auxLine = getTSString(timeClient.getEpochTime());
      strcpy(line, auxLine.c_str());
      file.printf("%s\n",line);
      
      //salvando identificação do log => evento
      file.printf("%s\n",flag);
      
      //salvando o conteudo do log => snap
      file.printf("%s\n",fileContend);
      
      file.close();
    }
}

void logPW(const char *flag){
  DynamicJsonDocument content(30);
  /*content["sampleI"] = sampleI;
  content["sampleV"] = sampleV;
  content["lastFilteredV"] = lastFilteredV; 
  content["filteredV"] = filteredV;
  content["filteredI"] = filteredI;
  content["offsetV"] = offsetV;
  content["offsetI"] = offsetI;
  content["phaseShiftedV"] = phaseShiftedV;
  content["sqV"] = sqV;
  content["sumV"] = sumV;
  content["sqI"] = sqI;
  content["sumI"] = sumI;
  content["instP"] = instP;
  content["sumP"] = sumP;
  content["startV"] = startV;
  content["lastVCross"] = lastVCross;
  content["checkVCross"] = checkVCross;
  content["realPower"] = realPower;
  content["apparentPower"] = apparentPower;
  content["powerFactor"] = powerFactor;
  content["Vrms"] = Vrms;
  content["Irms"] = Irms;
  content["SupplyVoltageV"] = SupplyVoltageV; 
  content["SupplyVoltageI"] = SupplyVoltageI;
  content["gmtOffset_sec"] = gmtOffset_sec; */
  //content["payload"] = payload;
  content["Vrms"] = Vrms; 
  char datacontent[30];
  serializeJson(content, datacontent);                  
  recordLog("Power", "-", flag);                         
}

void logCM(const char *flag){
  //DynamicJsonDocument content(900);
  char datacontent[30];
  sprintf(datacontent,"\"k\":%d",k);
  sprintf(datacontent,"%s, \"j\":%d",datacontent,j);
  //sprintf(datacontent,"%s, \"payload\":%s",datacontent,payload);
  //content["k"] = k;   
  //content["j"] = j;  
  //content["payload"] = payload; 
  
  //serializeJson(content, datacontent);                   
  recordLog("Com", "-", flag);                             
}


String getTSString(time_t rawtime) 
{

  //RtcDateTime now = Rtc.GetDateTime();
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

void storeDataEnergy(){
  File file = SPIFFS.open("/Store/powerMaxtrix.txt", "w");
    if (file) {
      for (int j = 0; j < powerline; j++){
        for (int i = 0; i < postsampling; i++) {
          file.printf("%u\n", power_matrix[j][i]);
          //data.add(power_matrix[j][i]);
        }
      }
      file.close();
    }
}

void loadDataEnergy(){
  File file = SPIFFS.open("/Store/powerMaxtrix.txt", "r");
    if (file) {
      for (int j = 0; j < powerline; j++){
        for (int i = 0; i < postsampling; i++) {
          power_matrix[j][i] = (file.readStringUntil('\n')).toInt();
        }
      }
      file.close();
    }
}
