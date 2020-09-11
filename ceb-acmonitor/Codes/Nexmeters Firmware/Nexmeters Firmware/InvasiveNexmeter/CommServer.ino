void DataToJson()
{
  DynamicJsonDocument doc(2000); // Cria JSON

  /* Le temperatura e umidade */
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  /* Se a leitura de temperatura e umidade falhar, recebe zero */
  if (isnan(humidity) || isnan(temperature)) {
    humidity = 0;
    temperature = 0;
  }

  /* Adiciona variaveis no JSON */
  doc["Id"] = WiFi.macAddress();
  doc["DataRegistro"] = getTimeStampString(k);

  JsonArray data = doc.createNestedArray("Potencias");

  for (int i = 0; i < postsampling; i++) {
    data.add(power_matrix[k][i]);
  }

  doc["Potencia"] = 0;
  doc["Temperatura"] = temperature;
  doc["Umidade"] = humidity;

  serializeJson(doc, payload);  // Converte JSON para vetor de char
}

void PostToServer()
{
  byte trypost = 0;

  while (true)
  {
    HTTPClient http;
    http.begin("http://nexsolar.sytes.net/chesp/api/consumo");
    http.addHeader("Content-Type", "application/json");             //Specify content-type header

    int httpResponseCode = http.POST(payload);   //Send the actual POST request

    Serial.println(payload);

    if (httpResponseCode == 200) {

      k++;
      break;
    }

    else
    {
      trypost++;
      if (trypost == 5)
      {
        reconnect();
        trypost = 0;
      }
    }

  }
}
