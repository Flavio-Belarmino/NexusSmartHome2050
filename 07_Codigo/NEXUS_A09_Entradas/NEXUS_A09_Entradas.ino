/* NEXUS | A09 R01 | Diagnostico de quatro entradas D36-D39.
 * Nao pressupoe modelo ou polaridade do modulo touch do inventario.
 */
#include <Arduino.h>
const uint8_t PINOS[4]={36,37,38,39};
bool habilitado=false;uint32_t ultimoLog=0;
void setup(){
  for(uint8_t i=0;i<4;++i)pinMode(PINOS[i],INPUT);
  Serial.begin(115200);Serial.println(F("A09: confirmar modulo, alimentacao e niveis antes de conectar; i habilita leitura; x suspende."));
}
void loop(){
  while(Serial.available()){char c=Serial.read();if(c=='i')habilitado=true;else if(c=='x')habilitado=false;}
  uint32_t agora=millis();if(static_cast<uint32_t>(agora-ultimoLog)<500)return;ultimoLog=agora;
  Serial.print(F("{\"module\":\"A09\",\"enabled\":"));Serial.print(habilitado?F("true"):F("false"));Serial.print(F(",\"raw_inputs\":["));
  for(uint8_t i=0;i<4;++i){if(i)Serial.print(',');if(habilitado)Serial.print(digitalRead(PINOS[i])==HIGH?1:0);else Serial.print(F("null"));}
  Serial.println(F("]}"));
}
