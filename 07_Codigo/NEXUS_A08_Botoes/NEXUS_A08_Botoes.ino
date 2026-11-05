/* Casa Inteligente | NEXUS | ExpoTech | A08 R01
 * Teste de 11 LEDs e 4 botoes, com entrada de parada logica em D3.
 * Nao substitui corte fisico independente de cargas.
 */
#include <Arduino.h>
const uint8_t LEDS[11]={22,23,24,25,26,27,28,29,30,31,32};
const uint8_t BOTOES[4]={40,41,42,43},PARADA=3;
bool estados[11]={false},bruto[4]={true,true,true,true},estavel[4]={true,true,true,true};
uint32_t mudou[4]={0},ultimoPasso=0,ultimoLog=0;
bool bloqueado=true,sequencia=false;int passo=-1;
void apagar(){for(uint8_t i=0;i<11;++i){estados[i]=false;digitalWrite(LEDS[i],LOW);}sequencia=false;passo=-1;}
void alternar(uint8_t i){if(!bloqueado){if(sequencia)apagar();estados[i]=!estados[i];}}
void setup(){
  for(uint8_t i=0;i<11;++i){digitalWrite(LEDS[i],LOW);pinMode(LEDS[i],OUTPUT);}
  for(uint8_t i=0;i<4;++i)pinMode(BOTOES[i],INPUT_PULLUP);
  pinMode(PARADA,INPUT_PULLUP);pinMode(LED_BUILTIN,OUTPUT);Serial.begin(115200);
  Serial.println(F("A08: inicia BLOQUEADO. D3 com contato NC para GND; r rearma; 1-4 alternam L01-L04; t sequencia; 0 apaga."));
}
void loop(){
  uint32_t agora=millis();
  if(digitalRead(PARADA)==HIGH){bloqueado=true;apagar();}
  while(Serial.available()){
    char c=Serial.read();
    if(c=='r' && digitalRead(PARADA)==LOW){bloqueado=false;apagar();}
    else if(c=='0')apagar();
    else if(c>='1'&&c<='4')alternar(c-'1');
    else if(c=='t' && !bloqueado){apagar();sequencia=true;passo=0;estados[0]=true;ultimoPasso=agora;}
  }
  for(uint8_t i=0;i<4;++i){
    bool valor=digitalRead(BOTOES[i])==HIGH;
    if(valor!=bruto[i]){bruto[i]=valor;mudou[i]=agora;}
    if(valor!=estavel[i] && static_cast<uint32_t>(agora-mudou[i])>=30){estavel[i]=valor;if(!valor)alternar(i);}
  }
  if(sequencia && static_cast<uint32_t>(agora-ultimoPasso)>=300){
    ultimoPasso=agora;estados[passo]=false;++passo;
    if(passo<11)estados[passo]=true;else{sequencia=false;passo=-1;}
  }
  for(uint8_t i=0;i<11;++i)digitalWrite(LEDS[i],!bloqueado&&estados[i]?HIGH:LOW);
  digitalWrite(LED_BUILTIN,bloqueado?HIGH:LOW);
  if(static_cast<uint32_t>(agora-ultimoLog)>=1000){
    ultimoLog=agora;Serial.print(F("{\"module\":\"A08\",\"stopped\":"));Serial.print(bloqueado?F("true"):F("false"));
    Serial.print(F(",\"leds\":["));for(uint8_t i=0;i<11;++i){if(i)Serial.print(',');Serial.print(!bloqueado&&estados[i]?1:0);}Serial.println(F("]}"));
  }
}
