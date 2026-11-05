/* Casa Inteligente | NEXUS | ExpoTech | A04 R01 | DHT22 em D34 */
#include <Arduino.h>
#include <DHT.h>
const uint8_t PIN_DHT=34;
DHT sensor(PIN_DHT,DHT22);
uint32_t ultimaLeitura=0;
uint16_t falhas=0;
void setup(){Serial.begin(115200);sensor.begin();Serial.println(F("A04: DHT22 D34; leitura a cada 2,5 segundos; saida JSON."));}
void loop(){
  uint32_t agora=millis();
  if(static_cast<uint32_t>(agora-ultimaLeitura)<2500)return;
  ultimaLeitura=agora;
  float umidade=sensor.readHumidity(), temperatura=sensor.readTemperature();
  bool valido=!isnan(umidade)&&!isnan(temperatura)&&umidade>=0&&umidade<=100&&temperatura>=-40&&temperatura<=80;
  if(valido)falhas=0;else if(falhas<65535)++falhas;
  Serial.print(F("{\"module\":\"A04\",\"ms\":"));Serial.print(agora);
  Serial.print(F(",\"valid\":"));Serial.print(valido?F("true"):F("false"));
  Serial.print(F(",\"temperature_c\":"));if(valido)Serial.print(temperatura,1);else Serial.print(F("null"));
  Serial.print(F(",\"humidity_pct\":"));if(valido)Serial.print(umidade,1);else Serial.print(F("null"));
  Serial.print(F(",\"consecutive_failures\":"));Serial.print(falhas);Serial.println(F("}"));
}
