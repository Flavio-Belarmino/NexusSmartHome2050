/* Casa Inteligente | NEXUS | ExpoTech | A02 R01
 * Bancada: microservo livre, sinal D6, LDR A0. Ler README antes de alimentar.
 * Inicia sem sinal de servo. Nao e controle integrado da casa.
 */
#include <Arduino.h>
#include <Servo.h>
Servo brise;
const uint8_t PIN_SERVO = 6, PIN_LDR = A0;
const int MINIMO = 60, CENTRO = 90, MAXIMO = 120;
int posicao = CENTRO, alvo = CENTRO, claro = -1, escuro = -1, leitura = 0;
bool habilitado = false, automatico = false, escuroAtivo = false;
uint32_t ultimaAmostra = 0, ultimoPasso = 0, ultimoLog = 0;

bool calibrado() { return claro >= 0 && escuro >= 0 && abs(claro-escuro) >= 80; }
void status() {
  Serial.print(F("{\"module\":\"A02\",\"enabled\":")); Serial.print(habilitado?F("true"):F("false"));
  Serial.print(F(",\"auto\":")); Serial.print(automatico?F("true"):F("false"));
  Serial.print(F(",\"angle_command_deg\":")); Serial.print(posicao);
  Serial.print(F(",\"target_deg\":")); Serial.print(alvo);
  Serial.print(F(",\"ldr\":")); Serial.print(leitura);
  Serial.print(F(",\"calibrated\":")); Serial.print(calibrado()?F("true"):F("false"));
  Serial.println(F("}"));
}
void setup() {
  pinMode(PIN_SERVO, INPUT); pinMode(PIN_LDR, INPUT);
  Serial.begin(115200); leitura=analogRead(PIN_LDR);
  Serial.println(F("A02: i habilita em 90 graus; x retira sinal; < 60; > 120; n 90; c claro; e escuro; a auto; s estado"));
}
void loop() {
  uint32_t agora=millis();
  if (static_cast<uint32_t>(agora-ultimaAmostra)>=50) {
    ultimaAmostra=agora; leitura=(3*leitura+analogRead(PIN_LDR))/4;
  }
  while (Serial.available()) {
    char c=Serial.read();
    if (c=='i' && !habilitado) { brise.attach(PIN_SERVO); brise.write(CENTRO); posicao=alvo=CENTRO; habilitado=true; }
    else if (c=='x') { brise.detach(); pinMode(PIN_SERVO,INPUT); habilitado=automatico=false; }
    else if (c=='<') { alvo=MINIMO; automatico=false; }
    else if (c=='>') { alvo=MAXIMO; automatico=false; }
    else if (c=='n') { alvo=CENTRO; automatico=false; }
    else if (c=='c') { claro=leitura; automatico=false; Serial.print(F("CLARO="));Serial.println(claro); }
    else if (c=='e') { escuro=leitura; automatico=false; Serial.print(F("ESCURO="));Serial.println(escuro); }
    else if (c=='a') { automatico=habilitado && calibrado(); if(!automatico)Serial.println(F("AUTO bloqueado: habilitar servo e calibrar primeiro.")); }
    else if (c=='s') status();
  }
  if (automatico) {
    int meio=(claro+escuro)/2;
    if (escuro>claro) {
      if(leitura>=meio+20)escuroAtivo=true; else if(leitura<=meio-20)escuroAtivo=false;
    } else {
      if(leitura<=meio-20)escuroAtivo=true; else if(leitura>=meio+20)escuroAtivo=false;
    }
    // Associacao inicial de bancada; o sentido do mecanismo real sera conferido.
    alvo=escuroAtivo?MINIMO:MAXIMO;
  }
  if(habilitado && static_cast<uint32_t>(agora-ultimoPasso)>=25) {
    ultimoPasso=agora;
    if(posicao<alvo)++posicao; else if(posicao>alvo)--posicao;
    brise.write(posicao);
  }
  if(static_cast<uint32_t>(agora-ultimoLog)>=1000){ultimoLog=agora;status();}
}
