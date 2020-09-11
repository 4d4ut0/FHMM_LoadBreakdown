boolean wifiConfig() 
{
  char ssid[20] = "Bruna";
  char password[20] = "bruna1993";

  //EEPROM.readString(0, ssid, 20);
  //EEPROM.readString(20, password, 20);
 

  unsigned long int currentTime = 0;

  Serial.printf("Connecting to: %s\n", ssid);
  Serial.printf("Password: %s\n", password);

  WiFi.begin(ssid, password);

  currentTime = millis();

  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
    delay(2000);
    Serial.print(".");
    if (millis() - currentTime > 360000) {
      Serial.println("Ligando AP...");
      ApWifiConfig();
      wifi_flag = 0;
      return 0;
    }
  }
  Serial.println("CONNECTED!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  WiFi.softAPdisconnect (true);
  WiFi.mode(WIFI_MODE_STA);
  // Inicia a rota "/turnon" que receberá um HTTP GET request
  server.on("/", HTTP_GET, turn_on_f);
  // Seta a função de Call Back para as rotas não encontradas
  server.onNotFound(notFound);
  // Inicia o web server
  server.begin();
  return 1;
}

void ApWifiConfig() {
  String MAC = WiFi.macAddress();
  MAC.replace(":", "-");
  MAC = "Inexmonitor_" + MAC;

  WiFi.softAP(MAC.c_str(), "nexsolar");
  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.mode(WIFI_MODE_AP);

  Serial.print("IP address: ");
  Serial.println(WiFi.softAPIP());

  // Inicia a rota "/turnon" que receberá um HTTP GET request
  server.on("/", HTTP_GET, turn_on_f);
  // Seta a função de Call Back para as rotas não encontradas
  server.onNotFound(notFound);
  // Inicia o web server
  server.begin();
}

void notFound(AsyncWebServerRequest *request) {
  request->send(404, "text/plain", "Not found");
}

/* http://192.168.4.1/?ssid=leonardo&password=123456&fuso=-4 */
void turn_on_f(AsyncWebServerRequest *request) {
  if (request->hasArg("ssid") && request->hasArg("password") && request->hasArg("fuso")) {
    request->send(200, "text/plain", "OK!");

    eepromWriteWifi(request->arg("ssid").c_str(), request->arg("password").c_str(), request->arg("fuso").c_str());
  }
  else if (request->hasArg("type")) {
    //eepromWriteType(request->arg("type").c_str());
    request->send(200, "text/plain", "Cadastrado!");
    deviceRegister(request->arg("type").c_str());
  }
  else if (request->hasArg("free") && WiFi.status() == WL_CONNECTED) {
    request->send(200, "text/plain", "CONECTADOO!");
    WiFi.softAPdisconnect(true);
    WiFi.mode(WIFI_MODE_STA);
    Serial.println("oi");
  }
  else {
    request->send(400, "text/plain", "Arg is missing");
  }
}

void eepromWriteWifi(const char *ssid, const char *password, const char *fuso) {
  int fuso_num = atoi(fuso);

  Serial.print("ssid: ");
  Serial.println(ssid);

  Serial.print("password: ");
  Serial.println(password);

  Serial.print("fuso: ");
  Serial.println(fuso_num);

  EEPROM.writeString (0, ssid);
  EEPROM.writeString (20, password);

  EEPROM.writeInt (90, fuso_num);

  EEPROM.commit();

  wifi_flag = 1;
}

void eepromWriteType(const char *type) {

  Serial.print("type: ");
  Serial.println(type);

  EEPROM.writeString (40, type);

  EEPROM.commit();

  wifi_flag = 1;
}

void deviceRegister(const char *type) {
  char payload[128];
  StaticJsonDocument<128> doc;

  Serial.println(type);

  doc["idHardware"] = WiFi.macAddress();
  doc["idEstacao"] = type;

  serializeJson(doc, payload);
  Serial.println(payload);

  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

    HTTPClient http;
    http.begin("http://nexsolar.sytes.net/ceb/api/estacao/finalizar-cadastro");  //Specify destination for HTTP request
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

   

  }
  else {
    Serial.println("Error in WiFi connection");
  }
}


void reconnect()
{
  char ssid[20] = "Bruna";
  char password[20] = "bruna1993";

  //EEPROM.readString(0, ssid, 20);
  //EEPROM.readString(20, password, 20);

  WiFi.mode(WIFI_OFF);
  delay(5000);
  WiFi.mode(WIFI_MODE_STA);
  delay(5000);
  WiFi.begin(ssid, password);
  delay(2000);
  while (WiFi.status() != WL_CONNECTED) {
  WiFi.begin(ssid, password);
  Serial.println("Reconectando");

    delay(5000);
  }
  Serial.println("CONNECTED!");
}
