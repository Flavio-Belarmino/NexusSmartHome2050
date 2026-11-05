/* Casa Inteligente | NEXUS | ExpoTech | A05 R01
 * Leitura de nivel e preparacao da medicao de pulsos.
 * A permissao da bomba e apenas logica: D8 permanece INPUT.
 */
#include <Arduino.h>
#include "controle_agua.h"
const uint8_t TRIG=10,ECHO=11,VAZAO=2,BOMBA=8;
// Alterar somente depois de identificar tensao/tipo de saida do sensor.
const bool VAZAO_CONFIRMADA=false;
// Zero significa fator ainda nao medido: sem conversao para litros.
const float PULSOS_POR_LITRO=0;
volatile uint32_t pulsos=0;
uint32_t ultimoContador=0,contadorVisto=0,ultimoPulso=0,ultimaLeitura=0,ultimoLog=0,janela=0;
float distancia=-1,vazio=-1,cheio=-1,vazaoLmin=-1;
bool permissao=false;
nexus::ControleAgua controle;
void contar(){++pulsos;}
uint32_t copiarPulsos(){noInterrupts();uint32_t p=pulsos;interrupts();return p;}
void setup(){
  pinMode(BOMBA,INPUT);pinMode(TRIG,OUTPUT);digitalWrite(TRIG,LOW);pinMode(ECHO,INPUT);
  pinMode(VAZAO,INPUT);pinMode(LED_BUILTIN,OUTPUT);digitalWrite(LED_BUILTIN,LOW);
  Serial.begin(115200);
  if(VAZAO_CONFIRMADA)attachInterrupt(digitalPinToInterrupt(VAZAO),contar,RISING);
  Serial.println(F("A05: v captura vazio; c captura cheio; p pede bomba LOGICA; 0 para; r rearma; D8 sem acionamento."));
}
void loop(){
  uint32_t agora=millis();
  if(static_cast<uint32_t>(agora-ultimaLeitura)>=200){
    ultimaLeitura=agora;digitalWrite(TRIG,LOW);delayMicroseconds(2);digitalWrite(TRIG,HIGH);delayMicroseconds(10);digitalWrite(TRIG,LOW);
    unsigned long duracao=pulseIn(ECHO,HIGH,25000UL);
    distancia=duracao?duracao/58.0f:-1;
    if(distancia<2 || distancia>400)distancia=-1;
  }
  uint32_t contador=copiarPulsos();
  if(contador!=contadorVisto){ultimoPulso=agora;contadorVisto=contador;}
  if(static_cast<uint32_t>(agora-janela)>=1000){
    float segundos=static_cast<uint32_t>(agora-janela)/1000.0f;
    vazaoLmin=VAZAO_CONFIRMADA && PULSOS_POR_LITRO>0 ? (contador-ultimoContador)*60.0f/(PULSOS_POR_LITRO*segundos):-1;
    ultimoContador=contador;janela=agora;
  }
  while(Serial.available()){
    char c=Serial.read();
    if(c=='v'){vazio=distancia;controle.calibrar(vazio,cheio);Serial.print(F("VAZIO_CM="));Serial.println(vazio);}
    else if(c=='c'){cheio=distancia;controle.calibrar(vazio,cheio);Serial.print(F("CHEIO_CM="));Serial.println(cheio);}
    else if(c=='p')controle.solicitar(true,agora);
    else if(c=='0')controle.solicitar(false,agora);
    else if(c=='r')controle.rearmar();
  }
  permissao=controle.atualizar(agora,distancia,VAZAO_CONFIRMADA,ultimoPulso);
  digitalWrite(LED_BUILTIN,permissao?HIGH:LOW);
  if(static_cast<uint32_t>(agora-ultimoLog)>=1000){
    ultimoLog=agora;Serial.print(F("{\"module\":\"A05\",\"distance_cm\":"));if(distancia>=0)Serial.print(distancia,1);else Serial.print(F("null"));
    Serial.print(F(",\"level_pct\":"));if(controle.nivelValido())Serial.print(controle.nivel(),1);else Serial.print(F("null"));
    Serial.print(F(",\"pulses\":"));Serial.print(contador);
    Serial.print(F(",\"flow_l_min\":"));if(vazaoLmin>=0)Serial.print(vazaoLmin,3);else Serial.print(F("null"));
    Serial.print(F(",\"flow_enabled\":"));Serial.print(VAZAO_CONFIRMADA?F("true"):F("false"));
    Serial.print(F(",\"pump_permission\":"));Serial.print(permissao?F("true"):F("false"));
    Serial.print(F(",\"fault\":"));Serial.print(controle.falha()?F("true"):F("false"));
    Serial.println(F(",\"actuator_enabled\":false}"));
  }
}
