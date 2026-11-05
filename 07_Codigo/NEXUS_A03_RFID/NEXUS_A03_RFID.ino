/* Casa Inteligente | NEXUS | ExpoTech | A03 R01
 * Leitura/cadastro voluntario de cartao em RAM. Autorizacao indicada no LED 13.
 * RC522 requer alimentacao e interface de niveis conferidas. Ler README.
 * D7 da solenoide nunca e acionado nesta versao.
 */
#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
const uint8_t PIN_SS=53, PIN_RST=49, PIN_SOLENOIDE=7;
MFRC522 leitor(PIN_SS,PIN_RST);
uint8_t uidPermitido[10]={0}, tamanhoPermitido=0;
bool pronto=false, cadastrar=false, acesso=false;
uint32_t inicioAcesso=0,ultimoLog=0;
void relatar(bool gravado){
  Serial.print(F("{\"module\":\"A03\",\"ready\":"));Serial.print(pronto?F("true"):F("false"));
  Serial.print(F(",\"registered_now\":"));Serial.print(gravado?F("true"):F("false"));
  Serial.print(F(",\"authorized\":"));Serial.print(acesso?F("true"):F("false"));
  Serial.println(F(",\"actuator_enabled\":false}"));
}
void setup(){
  pinMode(PIN_SOLENOIDE,INPUT);
  pinMode(PIN_RST,INPUT);pinMode(PIN_SS,INPUT);pinMode(50,INPUT);pinMode(51,INPUT);pinMode(52,INPUT);
  pinMode(LED_BUILTIN,OUTPUT);digitalWrite(LED_BUILTIN,LOW);
  Serial.begin(115200);
  Serial.println(F("A03: i inicia leitor apos conferir interface; g cadastra proximo cartao; c limpa; s estado. D7 sem acionamento."));
}
void loop(){
  while(Serial.available()){
    char c=Serial.read();
    if(c=='i'){
      SPI.begin();leitor.PCD_Init();
      uint8_t v=leitor.PCD_ReadRegister(MFRC522::VersionReg);
      pronto=v!=0 && v!=255;
      cadastrar=false;acesso=false;digitalWrite(LED_BUILTIN,LOW);
      Serial.print(F("LEITOR_VERSAO="));Serial.println(v,HEX);
      if(!pronto)Serial.println(F("Leitor sem resposta. Retirar alimentacao e revisar ligacoes."));
    } else if(c=='g' && pronto){cadastrar=true;Serial.println(F("CADASTRO: apresentar agora o cartao escolhido."));}
    else if(c=='c'){tamanhoPermitido=0;cadastrar=false;acesso=false;digitalWrite(LED_BUILTIN,LOW);Serial.println(F("Cadastro apagado da RAM."));}
    else if(c=='s'){Serial.print(F("pronto="));Serial.print(pronto);Serial.print(F(" cadastrado="));Serial.println(tamanhoPermitido>0);}
  }
  if(acesso && static_cast<uint32_t>(millis()-inicioAcesso)>=3000){acesso=false;digitalWrite(LED_BUILTIN,LOW);}
  if(static_cast<uint32_t>(millis()-ultimoLog)>=1000){ultimoLog=millis();relatar(false);}
  if(!pronto || !leitor.PICC_IsNewCardPresent() || !leitor.PICC_ReadCardSerial())return;
  uint8_t n=leitor.uid.size;
  bool valido=n>0 && n<=sizeof(uidPermitido);
  bool gravado=false;
  if(cadastrar && valido){
    tamanhoPermitido=n;for(uint8_t j=0;j<n;++j)uidPermitido[j]=leitor.uid.uidByte[j];
    cadastrar=false;gravado=true;
  }
  bool autorizado=valido && tamanhoPermitido==n;
  for(uint8_t j=0;j<n && autorizado;++j)if(uidPermitido[j]!=leitor.uid.uidByte[j])autorizado=false;
  // Nao libera na propria operacao de cadastro; testar depois, reapresentando o cartao.
  acesso=autorizado && !gravado;inicioAcesso=millis();digitalWrite(LED_BUILTIN,acesso?HIGH:LOW);
  relatar(gravado);ultimoLog=millis();
  leitor.PICC_HaltA();leitor.PCD_StopCrypto1();
}
