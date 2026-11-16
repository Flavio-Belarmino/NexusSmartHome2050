/*
  NEXUS - TFT integrado R06 - Arduino Mega 2560
  Bibliotecas: MCUFRIEND_kbv, Adafruit GFX Library, Adafruit TouchScreen,
  MFRC522, Servo e DHT sensor library (instalar dependencias solicitadas).
  Tela ILI9341 paralela, 320x240, rotacao 1.
  Calibracao real informada pelo grupo: 197,933,952,198.

  TFT: RD A0, WR A1, RS A2, CS A3, RST A4.
  D0 8, D1 9, D2 2, D3 3, D4 4, D5 5, D6 6, D7 7.
  TFT: 5V e GND. SD, F_CS e 3.3V desconectados.

  NOVOS PINOS: servo 30, botao portao 32, LED portao 33,
  LED LDR 34, higrometro A8, LDR A9.
  Anterior 25, proxima 26; LED amarelo permanece 28.
  Botoes opcionais: luz 35, bomba 36 (ambos para GND).

  Alimentacao externa: servo em uma fonte de 5 V; TFT em outra de 5 V.
  Unir os negativos (GND) das saidas DC e o GND do Mega.
  Manter separados os positivos das fontes e o 5 V do Mega.
  RFID continua em 3.3 V, com as reducoes de nivel ja montadas.

  R06: animacoes incrementais, com velocidade visual independente do servo.
  Portao desliza devagar; reservatorio azul com enchimento ilustrativo e onda.
  Lua/sol conforme LDR; termometro muda de azul a vermelho; apito intermitente original.
  Aviso global de falha DHT por 3 s, uma vez por episodio de falha.
  Clima: TESTAR aciona buzzer/LED por 3 s; SILENCIAR cancela teste/alarme.
  Botao fisico 24 tambem cancela o teste. Pinagens preservadas.
  Servo mantem passos por tempo decorrido; comandos/pinagens preservados.
  Relogio por software no inicio: parte da data/hora da compilacao.
  Ajustar no Serial (9600, Nova linha): H AAAA-MM-DD HH:MM:SS
  Sem RTC: reiniciar/desligar volta a data/hora da compilacao.
  RFID abre e fecha apos 3 s; se aberto/abrindo, RFID apenas fecha.
  Botao e TFT mantem o portao na posicao ate novo comando.

  As indicacoes de portao e bomba representam comandos.
  Nao ha sensor de posicao do portao nem feedback da bomba.
*/

#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <DHT.h>
#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <math.h>
#include <string.h>

const byte P_SERVO=30, P_PORTAO=32, P_LED_PORTAO=33;
const byte P_DHT=22, P_LED_ALARME=23, P_CANCELAR=24;
const byte P_ANTERIOR=25, P_PROXIMA=26, P_LED_AGUA=28;
const byte P_LUZ=34, P_BOTAO_LUZ=35, P_BOTAO_BOMBA=36;
const byte P_RELE=42, P_BOIA=43, P_BUZZER=44;
const byte P_RFID_RST=49, P_RFID_SS=53;
const byte P_HIGRO=A8, P_LDR=A9;

const byte RELE_ON=LOW, RELE_OFF=HIGH;
const byte LUZ_ON=LOW, LUZ_OFF=HIGH;
const int FECHADO=0, ABERTO=90;
const int AGUA_ON=800, AGUA_OFF=900;
const int LDR_ESCURO=400, LDR_CLARO=500;
const bool ESCURO_LEITURA_BAIXA=true;
const float ALARME_ON=30.0, ALARME_OFF=29.5;
// Servo: 1 grau a cada 10 ms; percurso 0-90 em cerca de 0,9 s.
const unsigned long PASSO_SERVO=10, ACOMODACAO=250;
const unsigned long ESPERA_PORTAO=3000, TROCA_PAGINA=3000;

const int XP=6, XM=A2, YP=A1, YM=7;
const int TS_LEFT=197, TS_RT=933, TS_TOP=952, TS_BOT=198;
const int PRESSAO_MIN=60, PRESSAO_MAX=1000;

const byte UID1[]={0x86,0x60,0x71,0x9E};
const byte UID2[]={0xDA,0x76,0xFA,0x55};

MCUFRIEND_kbv tela;
TouchScreen toque(XP,YP,XM,YM,300);
MFRC522 rfid(P_RFID_SS,P_RFID_RST);
Servo portao;
DHT dht(P_DHT,DHT22);

// Paleta RGB565: fundo azul-marinho, ciano, verde e amarelo.
const uint16_t FUNDO=0x0843, PAINEL=0x10A5, BORDA=0x21CB;
const uint16_t TEXTO=0xFFFF, CINZA=0x8493, CIANO=0x07FF;
const uint16_t VERDE=0x07E0, VERMELHO=0xF800, AMARELO=0xFFE0;
const uint16_t AZUL=0x001F, BRANCO=0xFFFF;

// Paginas: 0 inicio, 1 iluminacao, 2 garagem, 3 agua, 4 clima.
byte pagina=0;
bool apresentacao=true, desenharPagina=true, atualizarCabecalho=false;
unsigned long ultimaTroca=0, ultimaUI=0, ultimaAnimacao=0;
byte quadroAnimacao=0;
char cache[8][48]={{0}};
const char *titulos[]={"INICIO","ILUMINACAO","GARAGEM","AGUA","CLIMA / ALERTAS"};
char aviso[43]="Sistema iniciado";
unsigned long avisoAte=0;
bool avisoVisivel=false;

// Botoes fisicos: portao, cancelar, anterior, proxima, luz, bomba.
const byte botoes[]={P_PORTAO,P_CANCELAR,P_ANTERIOR,P_PROXIMA,P_BOTAO_LUZ,P_BOTAO_BOMBA};
bool anteriorBotao[6]={HIGH,HIGH,HIGH,HIGH,HIGH,HIGH};
bool estavelBotao[6]={HIGH,HIGH,HIGH,HIGH,HIGH,HIGH};
unsigned long mudouBotao[6]={0};

int posicao=FECHADO, destino=FECHADO;
bool movendo=false, fecharDepois=false, esperandoFechar=false;
unsigned long ultimoPasso=0, chegada=0, inicioEspera=0, inicioMovimento=0;

bool rfidOK=false;
unsigned long consultaRFID=0, tentativaRFID=0;

float temperatura=NAN, umidade=NAN;
bool dhtOK=false, quente=false, alarmeCancelado=false, faseAlarme=false;
bool testeAlarme=false;
unsigned long inicioTesteAlarme=0;
const unsigned long DURACAO_TESTE_ALARME=3000;
unsigned long leituraDHT=0, piscaAlarme=0;

int higro=1023, ldr=0;
bool vazamento=false, escuro=false, luzLigada=false;
unsigned long leituraAnalogica=0;

// Modos: 0 automatico, 1 desligado manual, 2 ligado manual.
byte modoLuz=0, modoBomba=0;
bool boiaAnterior=HIGH, boiaEstavel=HIGH, boiaValida=false;
bool bombaLigada=false;
unsigned long mudouBoia=0;

bool toqueTravado=false;
unsigned long ultimoContato=0, consultaToque=0;
unsigned long msgSensores=0, msgBoia=0;

// Estados exclusivamente visuais: nao sao medicao de posicao/nivel.
int anguloVisual=0, alturaPortaAnterior=-1;
int nivelVisual=0, alturaAguaAnterior=-1;
int ultimaLua=-1, alturaTermometroAnterior=-1;
uint16_t corTermometroAnterior=0;
int ondaAnterior[52];
byte faseOnda=0;
unsigned long animacaoPortao=0, animacaoAgua=0;
bool inicializarAnimacao=true;
bool falhaDHTAvisada=false, avisoDHTAtivo=false, avisoDHTDesenhado=false;
unsigned long fimAvisoDHT=0;

// Relogio por software: independente da velocidade do loop e das paginas.
unsigned int anoRelogio=2026;
byte mesRelogio=1, diaRelogio=1;
unsigned long segundosDoDia=0, baseRelogio=0;
unsigned long segundoDesenhado=86400UL;
char entradaSerial[40]={0};
byte tamanhoEntrada=0;
bool entradaLonga=false;

bool bissexto(unsigned int ano) {
  return ano%4==0 && (ano%100!=0 || ano%400==0);
}

byte diasDoMes(byte mes,unsigned int ano) {
  const byte dias[]={31,28,31,30,31,30,31,31,30,31,30,31};
  if(mes<1 || mes>12) return 0;
  return dias[mes-1]+(mes==2 && bissexto(ano) ? 1 : 0);
}

void iniciarRelogio() {
  char mes[4]={0};
  unsigned int dia=1,ano=2026,h=0,m=0,seg=0;
  sscanf(__DATE__,"%3s %u %u",mes,&dia,&ano);
  sscanf(__TIME__,"%u:%u:%u",&h,&m,&seg);
  const char *nomes="JanFebMarAprMayJunJulAugSepOctNovDec";
  byte numeroMes=1;
  for(byte i=0;i<12;i++) {
    if(strncmp(mes,nomes+i*3,3)==0) {numeroMes=i+1;break;}
  }
  anoRelogio=ano;mesRelogio=numeroMes;diaRelogio=dia;
  segundosDoDia=h*3600UL+m*60UL+seg;
  baseRelogio=millis();
}

void atualizarRelogio() {
  unsigned long agora=millis();
  unsigned long decorrido=(agora-baseRelogio)/1000UL;
  if(!decorrido) return;
  baseRelogio+=decorrido*1000UL;
  segundosDoDia+=decorrido;
  while(segundosDoDia>=86400UL) {
    segundosDoDia-=86400UL;
    diaRelogio++;
    if(diaRelogio>diasDoMes(mesRelogio,anoRelogio)) {
      diaRelogio=1;
      if(++mesRelogio>12) {mesRelogio=1;anoRelogio++;}
    }
  }
}

bool ajustarRelogio(const char *linha) {
  unsigned int a,mes,d,h,m,seg;
  char extra;
  if(sscanf(linha,"H %u-%u-%u %u:%u:%u %c",
            &a,&mes,&d,&h,&m,&seg,&extra)!=6) return false;
  if(a<2020 || a>2099 || mes<1 || mes>12 || d<1 ||
     d>diasDoMes(mes,a) || h>23 || m>59 || seg>59) return false;
  anoRelogio=a;mesRelogio=mes;diaRelogio=d;
  segundosDoDia=h*3600UL+m*60UL+seg;
  baseRelogio=millis();
  segundoDesenhado=86400UL;
  return true;
}

void lerAjusteRelogio() {
  // Leitura sem esperar por texto: nao usa readString nem timeout.
  byte limite=32;
  while(Serial.available() && limite--) {
    char c=Serial.read();
    if(c=='\r') continue;
    if(c=='\n') {
      if(tamanhoEntrada || entradaLonga) {
        entradaSerial[tamanhoEntrada]=0;
        if(!entradaLonga && ajustarRelogio(entradaSerial))
          Serial.println(F("[RELOGIO] Data e hora ajustadas."));
        else Serial.println(F("Use: H AAAA-MM-DD HH:MM:SS"));
      }
      tamanhoEntrada=0;entradaLonga=false;
    } else if(tamanhoEntrada<sizeof(entradaSerial)-1) {
      entradaSerial[tamanhoEntrada++]=c;
    } else entradaLonga=true;
  }
}

void limparCache() {
  memset(cache,0,sizeof(cache));
}

void notificar(const char *texto) {
  strncpy(aviso,texto,sizeof(aviso)-1);
  aviso[sizeof(aviso)-1]=0;
  avisoAte=millis()+3500;
  Serial.println(aviso);
  // Forca atualizacao da faixa, mesmo se o aviso anterior estiver visivel.
  cache[7][0]=0;
}

void pausarApresentacao() {
  if (apresentacao) {
    apresentacao=false;
    atualizarCabecalho=true;
  }
}

void mudarPagina(int direcao, bool manual) {
  if (manual) pausarApresentacao();
  pagina=(pagina+direcao+5)%5;
  ultimaTroca=millis();
  desenharPagina=true;
}

bool pressionou(byte i) {
  unsigned long agora=millis();
  bool leitura=digitalRead(botoes[i]);
  if (leitura!=anteriorBotao[i]) {
    anteriorBotao[i]=leitura;
    mudouBotao[i]=agora;
  }
  if (agora-mudouBotao[i]>=40 && leitura!=estavelBotao[i]) {
    estavelBotao[i]=leitura;
    return leitura==LOW;
  }
  return false;
}

int mediaAnalogica(byte pino) {
  analogRead(pino);
  long soma=0;
  for(byte i=0;i<10;i++) soma+=analogRead(pino);
  return soma/10;
}

void moverPortao(int alvo, bool automatico) {
  fecharDepois=automatico;
  esperandoFechar=false;
  if (destino==alvo && !movendo && posicao==alvo) {
    if (alvo==ABERTO && automatico) {
      esperandoFechar=true;
      inicioEspera=millis();
    }
    return;
  }
  destino=alvo;
  movendo=true;
  ultimoPasso=chegada=inicioMovimento=millis();
  digitalWrite(P_LED_PORTAO,HIGH);
  notificar(alvo==ABERTO ? "Portao: abrindo" : "Portao: fechando");
}

void alternarPortao() {
  moverPortao(destino==ABERTO ? FECHADO : ABERTO,false);
}

void atualizarPortao() {
  unsigned long agora=millis();
  if (posicao!=destino && agora-ultimoPasso>=PASSO_SERVO) {
    // Recupera os passos decorridos mesmo se houve uma operacao mais lenta.
    // A versao anterior avancava apenas 1 grau a cada passagem pelo loop.
    unsigned long decorridos=(agora-ultimoPasso)/PASSO_SERVO;
    int restantes=abs(destino-posicao);
    int passos=decorridos>(unsigned long)restantes ? restantes : (int)decorridos;
    ultimoPasso+=(unsigned long)passos*PASSO_SERVO;
    posicao+=(destino>posicao ? passos : -passos);
    portao.write(posicao);
    if (posicao==destino) chegada=agora;
  }
  if (movendo && posicao==destino && agora-chegada>=ACOMODACAO) {
    movendo=false;
    digitalWrite(P_LED_PORTAO,LOW);
    Serial.print(F("[SERVO] Comando concluido em "));
    Serial.print(agora-inicioMovimento);
    Serial.println(F(" ms (inclui 250 ms de acomodacao; sem sensor de posicao)."));
    if (destino==ABERTO && fecharDepois) {
      esperandoFechar=true;
      inicioEspera=agora;
    }
    if (destino==FECHADO) {
      fecharDepois=false;
      esperandoFechar=false;
    }
  }
  if (esperandoFechar && agora-inicioEspera>=ESPERA_PORTAO) {
    moverPortao(FECHADO,false);
  }
}

bool uidAutorizado() {
  if (rfid.uid.size!=4) return false;
  bool a=true,b=true;
  for(byte i=0;i<4;i++) {
    if (rfid.uid.uidByte[i]!=UID1[i]) a=false;
    if (rfid.uid.uidByte[i]!=UID2[i]) b=false;
  }
  return a||b;
}

void inicializarRFID() {
  rfid.PCD_Init();
  byte versao=rfid.PCD_ReadRegister(MFRC522::VersionReg);
  rfidOK=(versao!=0 && versao!=255);
  tentativaRFID=millis();
}

void atualizarRFID() {
  unsigned long agora=millis();
  if (!rfidOK) {
    if (agora-tentativaRFID>=5000) inicializarRFID();
    return;
  }
  if (agora-consultaRFID<50) return;
  consultaRFID=agora;
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) return;
  bool liberado=uidAutorizado();
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
  if (!liberado) {
    notificar("RFID: acesso negado");
    return;
  }
  if (destino==ABERTO) moverPortao(FECHADO,false);
  else moverPortao(ABERTO,true);
}

void saidasAlarme() {
  // Apito original: 2000 Hz por 250 ms, seguido de 250 ms de silencio.
  bool ligado=((quente && !alarmeCancelado) || testeAlarme) && faseAlarme;
  digitalWrite(P_LED_ALARME,ligado ? HIGH : LOW);
  if(ligado) tone(P_BUZZER,2000);
  else {
    noTone(P_BUZZER);
    digitalWrite(P_BUZZER,LOW);
  }
}

void cancelarAlarme() {
  if(quente || testeAlarme) {
    if(quente) alarmeCancelado=true;
    testeAlarme=false;
    faseAlarme=false;
    saidasAlarme();
    notificar(quente ? "Alarme cancelado; aguarda esfriar" : "Teste do alarme cancelado");
  } else notificar("Nenhum alarme de temperatura ativo");
}

void alternarTesteAlarme() {
  if(testeAlarme) {
    testeAlarme=false;
    if(!quente || alarmeCancelado) faseAlarme=false;
    saidasAlarme();
    notificar("Teste do alarme interrompido");
    return;
  }
  testeAlarme=true;
  inicioTesteAlarme=piscaAlarme=millis();
  faseAlarme=true;
  saidasAlarme();
  notificar("Teste: buzzer e LED por 3 segundos");
}

void atualizarTemperatura() {
  unsigned long agora=millis();
  // DHT bloqueia interrupcoes brevemente. Evita ler durante o giro.
  if (movendo || agora-leituraDHT<2500) return;
  leituraDHT=agora;
  temperatura=dht.readTemperature();
  umidade=dht.readHumidity();
  dhtOK=!isnan(temperatura);
  if (!dhtOK) {
    // Um aviso por episodio, sem repetir a cada leitura invalida.
    // O ultimo estado do alarme permanece preservado.
    if(!falhaDHTAvisada) {
      falhaDHTAvisada=true;
      avisoDHTAtivo=true;
      avisoDHTDesenhado=false;
      fimAvisoDHT=millis()+3000UL;
      Serial.println(F("[DHT] Sem leitura de temperatura. Verifique sensor e conexoes."));
    }
    return;
  }
  falhaDHTAvisada=false;
  if (!quente && temperatura>=ALARME_ON) {
    quente=true;
    alarmeCancelado=false;
    faseAlarme=true;
    piscaAlarme=millis();
    saidasAlarme();
    notificar("ALERTA: temperatura a partir de 30 C");
  } else if (quente && temperatura<=ALARME_OFF) {
    quente=false;
    alarmeCancelado=false;
    if(!testeAlarme) faseAlarme=false;
    saidasAlarme();
    notificar("Temperatura normal: alarme rearmado");
  }
}

void atualizarAlarme() {
  unsigned long agora=millis();
  if(testeAlarme && agora-inicioTesteAlarme>=DURACAO_TESTE_ALARME) {
    testeAlarme=false;
    if(!quente || alarmeCancelado) faseAlarme=false;
    saidasAlarme();
    notificar("Teste do alarme concluido");
  }
  if(((quente && !alarmeCancelado) || testeAlarme) && agora-piscaAlarme>=250) {
    piscaAlarme=agora;
    faseAlarme=!faseAlarme;
    saidasAlarme();
  }
}

void atualizarAnalogicos() {
  if (millis()-leituraAnalogica<100) return;
  leituraAnalogica=millis();
  higro=mediaAnalogica(P_HIGRO);
  ldr=mediaAnalogica(P_LDR);
  if (higro<=AGUA_ON) vazamento=true;
  else if (higro>=AGUA_OFF) vazamento=false;
  digitalWrite(P_LED_AGUA,vazamento ? HIGH : LOW);
  if (ESCURO_LEITURA_BAIXA) {
    if (ldr<=LDR_ESCURO) escuro=true;
    else if (ldr>=LDR_CLARO) escuro=false;
  } else {
    if (ldr>=LDR_CLARO) escuro=true;
    else if (ldr<=LDR_ESCURO) escuro=false;
  }
  luzLigada=(modoLuz==0 ? escuro : modoLuz==2);
  digitalWrite(P_LUZ,luzLigada ? LUZ_ON : LUZ_OFF);
}

void atualizarBomba() {
  unsigned long agora=millis();
  bool leitura=digitalRead(P_BOIA);
  if (leitura!=boiaAnterior) {
    boiaAnterior=leitura;
    mudouBoia=agora;
  }
  // Nivel cheio desliga imediatamente. Religamento exige estabilidade.
  if (leitura==HIGH) {
    bombaLigada=false;
    digitalWrite(P_RELE,RELE_OFF);
  }
  if (agora-mudouBoia<200) return;
  boiaEstavel=leitura;
  boiaValida=true;
  // HIGH = nivel atingido. Nenhum modo manual pode ignorar a boia.
  bombaLigada=boiaValida && boiaEstavel==LOW && modoBomba!=1;
  digitalWrite(P_RELE,bombaLigada ? RELE_ON : RELE_OFF);
}

void ajustarModoLuz(byte modo) {
  modoLuz=modo;
  // Aplica imediatamente, sem esperar a proxima leitura analogica.
  luzLigada=(modoLuz==0 ? escuro : modoLuz==2);
  digitalWrite(P_LUZ,luzLigada ? LUZ_ON : LUZ_OFF);
  notificar(modo==0 ? "Luz: automatico pelo LDR" : (modo==1 ? "Luz: comando manual desligado" : "Luz: comando manual ligado"));
}

void ajustarModoBomba(byte modo) {
  modoBomba=modo;
  atualizarBomba();
  if (modo==2 && (!boiaValida || digitalRead(P_BOIA)==HIGH))
    notificar("Bomba bloqueada: nivel cheio/pendente");
  else notificar(modo==0 ? "Bomba: modo automatico" : (modo==1 ? "Bomba: comando manual desligado" : "Bomba: manual com protecao da boia"));
}

void lerBotoes() {
  if (pressionou(0)) {pausarApresentacao(); alternarPortao();}
  if (pressionou(1)) {pausarApresentacao(); cancelarAlarme();}
  if (pressionou(2)) mudarPagina(-1,true);
  if (pressionou(3)) mudarPagina(1,true);
  if (pressionou(4)) {pausarApresentacao(); ajustarModoLuz((modoLuz+1)%3);}
  if (pressionou(5)) {pausarApresentacao(); ajustarModoBomba((modoBomba+1)%3);}
}

// ================= DESENHO DA INTERFACE =================

void texto(int x,int y,const char *s,byte tamanho,uint16_t cor) {
  tela.setTextSize(tamanho);
  tela.setTextColor(cor);
  tela.setCursor(x,y);
  tela.print(s);
}

void centralizar(int x,int y,int largura,const char *s,byte tamanho,uint16_t cor) {
  texto(x+(largura-(int)strlen(s)*6*tamanho)/2,y,s,tamanho,cor);
}

void botao(int x,int y,int w,int h,const char *rotulo,bool ativo,uint16_t cor) {
  tela.fillRoundRect(x,y,w,h,7,ativo ? cor : PAINEL);
  tela.drawRoundRect(x,y,w,h,7,cor);
  centralizar(x,y+(h-16)/2,w,rotulo,2,ativo ? FUNDO : TEXTO);
}

void botaoCache(byte slot,int x,int y,int w,int h,const char *rotulo,bool ativo,uint16_t cor) {
  char chave[32];
  snprintf(chave,sizeof(chave),"%d:%u:%s",ativo,cor,rotulo);
  if (!strcmp(cache[slot],chave)) return;
  strncpy(cache[slot],chave,31); cache[slot][31]=0;
  botao(x,y,w,h,rotulo,ativo,cor);
}

void valor(byte slot,int x,int y,int w,int h,const char *rotulo,const char *conteudo,uint16_t cor) {
  char chave[32];
  snprintf(chave,sizeof(chave),"%u:%s",cor,conteudo);
  if (!strcmp(cache[slot],chave)) return;
  strncpy(cache[slot],chave,31); cache[slot][31]=0;
  tela.fillRoundRect(x,y,w,h,7,PAINEL);
  tela.drawRoundRect(x,y,w,h,7,BORDA);
  tela.fillRect(x+8,y+10,3,h-20,cor);
  byte tam=(strlen(conteudo)*12U>(unsigned int)(w-24)) ? 1 : 2;
  if (h<40) {
    texto(x+18,y+(h-8*tam)/2,conteudo,tam,cor);
  } else {
    texto(x+18,y+9,rotulo,1,CINZA);
    texto(x+18,y+29,conteudo,tam,cor);
  }
}

uint16_t corTemperatura(float t) {
  if(isnan(t)) return CINZA;
  if(t<=18) return AZUL;
  if(t>=30) return VERMELHO;
  int r=0,g=0,b=255;
  if(t<22) g=(int)((t-18)*255/4);
  else if(t<26) {r=(int)((t-22)*255/4);g=255;b=255-r;}
  else {r=255;g=(int)((30-t)*255/4);b=0;}
  return tela.color565(r,g,b);
}

void numeroTemperatura(char *buf,byte n) {
  if (!dhtOK) {strncpy(buf,"SEM LEITURA",n); buf[n-1]=0; return;}
  char num[12]; dtostrf(temperatura,4,1,num);
  snprintf(buf,n,"%s C",num);
}

const char *estadoPortao() {
  if (movendo) return destino==ABERTO ? "ABRINDO" : "FECHANDO";
  return posicao==ABERTO ? "ABERTO" : "FECHADO";
}

void desenhoCasa(int x,int y,uint16_t cor) {
  tela.drawLine(x,y+16,x+18,y,cor);
  tela.drawLine(x+18,y,x+36,y+16,cor);
  tela.drawRect(x+5,y+16,26,22,cor);
  tela.drawRect(x+15,y+25,8,13,cor);
}

void desenharRelogio() {
  if(pagina!=0 || segundoDesenhado==segundosDoDia) return;
  segundoDesenhado=segundosDoDia;
  char data[12],hora[10];
  snprintf(data,sizeof(data),"%02u/%02u/%04u",
           (unsigned int)diaRelogio,(unsigned int)mesRelogio,anoRelogio);
  unsigned int h=segundosDoDia/3600UL;
  unsigned int m=(segundosDoDia/60UL)%60;
  unsigned int seg=segundosDoDia%60;
  snprintf(hora,sizeof(hora),"%02u:%02u:%02u",h,m,seg);
  tela.fillRect(85,0,150,32,PAINEL);
  centralizar(85,2,150,data,1,CINZA);
  centralizar(85,14,150,hora,2,TEXTO);
}

void desenharBase() {
  tela.fillScreen(FUNDO);
  tela.fillRect(0,0,320,32,PAINEL);
  texto(10,8,"NEXUS",2,CIANO);
  if(pagina!=0) texto(87,12,titulos[pagina],1,TEXTO);
  segundoDesenhado=86400UL;
  tela.fillRoundRect(257,5,56,22,5,apresentacao ? VERDE : AZUL);
  centralizar(257,12,56,apresentacao ? "AUTO" : "PAUSA",1,apresentacao ? FUNDO : BRANCO);
  tela.drawFastHLine(0,35,320,BORDA);
  botao(5,209,95,27,"< ANT",false,CIANO);
  botao(105,209,110,27,"INICIO",false,CIANO);
  botao(220,209,95,27,"PROX >",false,CIANO);
  limparCache();
  if (pagina==1) {
    texto(86,47,"ILUMINACAO DA CASA",1,CINZA);
  } else if (pagina==2) {
    texto(12,46,"POSICAO COMANDADA",1,CINZA);
  } else if (pagina==3) {
    texto(12,43,"RESERVATORIO",1,CINZA);
  } else if (pagina==4) {
    texto(12,46,"CONFORTO E ALERTAS",1,CINZA);
    tela.drawRoundRect(20,75,24,61,9,CINZA);
  }
  atualizarCabecalho=false;
  inicializarAnimacao=true;
  alturaPortaAnterior=-1;alturaAguaAnterior=-1;
  ultimaLua=-1;alturaTermometroAnterior=-1;
  for(byte i=0;i<52;i++) ondaAnterior[i]=-1;
  desenharPagina=false;
}

void desenharConteudo() {
  char a[26],b[26];
  numeroTemperatura(a,sizeof(a));
  if (pagina==0) {
    valor(0,8,44,148,63,"TEMPERATURA",a,corTemperatura(temperatura));
    valor(1,164,44,148,63,"PORTAO / COMANDO",estadoPortao(),VERDE);
    valor(2,8,116,148,63,"BOMBA / COMANDO",bombaLigada ? "LIGADA" : "DESLIGADA",bombaLigada ? CIANO : CINZA);
    valor(3,164,116,148,63,"VAZAMENTO",vazamento ? "DETECTADO" : "SECO",vazamento ? AMARELO : VERDE);
  } else if (pagina==1) {
    snprintf(a,sizeof(a),"%d",ldr);
    valor(0,86,62,226,55,"LEITURA LDR",a,AMARELO);
    const char *modo=modoLuz==0 ? "AUTO LDR" : "MANUAL";
    snprintf(a,sizeof(a),"%s / %s",modo,luzLigada ? "ON" : "OFF");
    valor(1,86,122,226,30,"",a,luzLigada ? AMARELO : CINZA);
    botaoCache(2,8,158,148,29,"AUTO LDR",modoLuz==0,CIANO);
    botaoCache(3,164,158,148,29,luzLigada ? "DESLIGAR" : "LIGAR",modoLuz!=0,AMARELO);
  } else if (pagina==2) {
    snprintf(a,sizeof(a),"%d graus",posicao);
    valor(0,8,64,104,65,"SERVO",a,CIANO);
    valor(1,8,133,304,22,"",estadoPortao(),movendo ? AMARELO : VERDE);
    botaoCache(2,8,158,148,29,"ABRIR",destino==ABERTO,VERDE);
    botaoCache(3,164,158,148,29,"FECHAR",destino==FECHADO,CIANO);
  } else if (pagina==3) {
    const char *nivel=!boiaValida ? "AGUARDE" : (boiaEstavel ? "CHEIO" : "ABAIXO");
    valor(0,106,43,206,52,"BOIA",nivel,boiaEstavel ? VERDE : CIANO);
    valor(1,106,100,206,52,"VAZAMENTO",vazamento ? "DETECTADO" : "SECO",vazamento ? AMARELO : VERDE);
    const char *rotulo=modoBomba==0 ? "AUTO" : (modoBomba==1 ? "MANUAL OFF" : "MANUAL ON");
    botaoCache(2,8,158,148,29,rotulo,modoBomba==0,CIANO);
    const char *acao=bombaLigada ? "DESLIGAR" : (modoBomba==2 ? "CANCELAR" : "LIGAR");
    botaoCache(3,164,158,148,29,acao,bombaLigada,VERDE);
  } else if (pagina==4) {
    valor(0,61,63,251,53,"TEMPERATURA",a,corTemperatura(temperatura));
    if (isnan(umidade)) strcpy(b,"SEM LEITURA");
    else {char num[12]; dtostrf(umidade,4,1,num); snprintf(b,sizeof(b),"%s %%",num);}
    const char *estado=testeAlarme ? "TESTANDO" : (quente ? (alarmeCancelado ? "CANCELADO" : "ALARME ATIVO") : "NORMAL");
    snprintf(a,sizeof(a),"%s | %s",b,estado);
    valor(1,61,121,251,31,"",a,quente ? AMARELO : VERDE);
    botaoCache(2,8,158,148,29,testeAlarme ? "PARAR" : "TESTAR",testeAlarme,AMARELO);
    botaoCache(3,164,158,148,29,"SILENCIAR",(quente && !alarmeCancelado) || testeAlarme,VERMELHO);
  }
  // Faixa de mensagens/estado sempre fora dos botoes de comando.
  bool visivel=(long)(avisoAte-millis())>0;
  char linha[43];
  if (visivel) strncpy(linha,aviso,sizeof(linha));
  else snprintf(linha,sizeof(linha),"%d/5 | RFID %s | %s",pagina+1,rfidOK ? "OK" : "FALHA",apresentacao ? "Toque para pausar" : "AUTO no topo retoma");
  linha[42]=0;
  // Cache separado: evita limpar/reimprimir a faixa em cada passagem.
  if (strcmp(cache[7],linha) || avisoVisivel!=visivel) {
    tela.fillRect(0,189,320,16,FUNDO);
    texto(7,194,linha,1,visivel ? AMARELO : CINZA);
    strncpy(cache[7],linha,47); cache[7][47]=0;
    avisoVisivel=visivel;
  }
}

void desenharAstro() {
  int lua=escuro ? 1 : 0;
  if(lua==ultimaLua) return;
  ultimaLua=lua;
  tela.fillRect(9,51,76,76,FUNDO);
  if(lua) {
    // Lua minguante preenchida: disco branco recortado pelo fundo.
    tela.fillCircle(45,89,23,BRANCO);
    tela.fillCircle(57,81,23,FUNDO);
  } else {
    tela.fillCircle(47,89,18,AMARELO);
    for(byte i=0;i<8;i++) {
      float a=i*0.7853982;
      tela.drawLine(47+cos(a)*24,89+sin(a)*24,
                    47+cos(a)*32,89+sin(a)*32,AMARELO);
    }
  }
}

void animarPortao(unsigned long agora) {
  if(agora-animacaoPortao>=80) {
    animacaoPortao=agora;
    // Apenas o desenho leva cerca de 3,6 s; motor continua com 0,9 s.
    if(anguloVisual<destino) anguloVisual=min(anguloVisual+2,destino);
    else if(anguloVisual>destino) anguloVisual=max(anguloVisual-2,destino);
  }
  int altura=map(anguloVisual,FECHADO,ABERTO,59,3);
  if(altura==alturaPortaAnterior) return;
  if(alturaPortaAnterior<0) {
    tela.drawRect(128,63,176,64,CIANO);
    tela.fillRect(132,66,168,59,FUNDO);
    alturaPortaAnterior=0;
  }
  if(altura>alturaPortaAnterior) {
    // Desenha somente as linhas novas ao descer.
    for(int y=alturaPortaAnterior;y<altura;y++)
      tela.drawFastHLine(132,66+y,168,y%7==3 ? CIANO : AZUL);
  } else {
    // Apaga somente as linhas que a porta deixou de ocupar.
    tela.fillRect(132,66+altura,168,alturaPortaAnterior-altura,FUNDO);
  }
  alturaPortaAnterior=altura;
  tela.fillCircle(296,137,3,anguloVisual!=destino ? AMARELO : VERDE);
}

void animarReservatorio(unsigned long agora) {
  if(agora-animacaoAgua>=160) {
    animacaoAgua=agora;
    // Ilustracao: a boia nao mede porcentagem. Sem valores percentuais na UI.
    if(boiaValida && boiaEstavel==HIGH) nivelVisual=min(nivelVisual+2,100);
    else if(bombaLigada) nivelVisual=min(nivelVisual+1,85);
    else if(boiaValida && nivelVisual>15) nivelVisual--;
    faseOnda=(faseOnda+1)%16;
  }
  int altura=map(nivelVisual,0,100,0,59);
  if(alturaAguaAnterior<0) {
    tela.fillRect(26,69,52,64,FUNDO);
    tela.drawRoundRect(22,65,60,71,5,CIANO);
    alturaAguaAnterior=0;
  }
  // Restaura a linha da onda anterior antes de mudar o nivel.
  for(byte x=0;x<52;x++) {
    if(ondaAnterior[x]>=69) {
      uint16_t fundo=ondaAnterior[x]>=132-alturaAguaAnterior ? AZUL : FUNDO;
      tela.drawPixel(26+x,ondaAnterior[x],fundo);
    }
  }
  if(altura>alturaAguaAnterior)
    tela.fillRect(26,132-altura,52,altura-alturaAguaAnterior,AZUL);
  else if(altura<alturaAguaAnterior)
    tela.fillRect(26,132-alturaAguaAnterior,52,alturaAguaAnterior-altura,FUNDO);
  alturaAguaAnterior=altura;
  // O perfil avanca para a direita: pequena onda sobre a agua azul.
  const int8_t onda[]={0,1,1,2,2,2,1,1,0,-1,-1,-2,-2,-2,-1,-1};
  for(byte x=0;x<52;x++) {
    ondaAnterior[x]=-1;
    if(altura>2) {
      int y=constrain(132-altura+onda[(x+16-faseOnda)%16],69,131);
      ondaAnterior[x]=y;
      tela.drawPixel(26+x,y,CIANO);
    }
  }
  // Tubo azul e gotas indo da esquerda para a direita.
  tela.fillRect(83,80,13,5,FUNDO);
  tela.drawFastHLine(83,82,13,AZUL);
  if(bombaLigada) tela.fillCircle(85+faseOnda%9,82,1,CIANO);
  // Rodape local com fundo para nao deixar letras antigas.
  tela.setTextSize(1);tela.setTextColor(bombaLigada ? AZUL : CINZA,FUNDO);
  tela.setCursor(24,142);tela.print(bombaLigada ? "BOMBA ON " : "BOMBA OFF");
}

void animarTermometro() {
  int h=dhtOK ? constrain((int)((temperatura-15)*2),0,44) : 0;
  uint16_t cor=corTemperatura(temperatura);
  if(h==alturaTermometroAnterior && cor==corTermometroAnterior) return;
  tela.fillRect(28,83,8,44,FUNDO);
  if(h) tela.fillRect(28,127-h,8,h,cor);
  tela.fillCircle(32,135,12,cor);
  alturaTermometroAnterior=h;corTermometroAnterior=cor;
}

void animarPagina() {
  unsigned long agora=millis();
  if(agora-ultimaAnimacao<80 && !inicializarAnimacao) return;
  ultimaAnimacao=agora;
  quadroAnimacao++;
  tela.fillCircle(244,15,3,(quadroAnimacao%10<5) ? CIANO : BORDA);
  if(pagina==1) desenharAstro();
  else if(pagina==2) animarPortao(agora);
  else if(pagina==3) animarReservatorio(agora);
  else if(pagina==4) animarTermometro();
  inicializarAnimacao=false;
  if(apresentacao && !movendo) {
    int w=constrain((int)((agora-ultimaTroca)*320UL/TROCA_PAGINA),0,320);
    tela.drawFastHLine(0,204,320,BORDA);
    if(w) tela.drawFastHLine(0,204,w,CIANO);
  }
}

void tratarToque(int x,int y) {
  if(avisoDHTAtivo && y>=36 && y<80) return;
  if (y<33 && x>=250) {
    apresentacao=!apresentacao;
    ultimaTroca=millis();
    desenharPagina=true;
    return;
  }
  pausarApresentacao();
  if (y>=207) {
    if (x<102) mudarPagina(-1,true);
    else if (x>=218) mudarPagina(1,true);
    else {pagina=0; desenharPagina=true;}
    return;
  }
  if (pagina==0 && y>=44 && y<=179) {
    if(y<110) pagina=(x<160 ? 4 : 2);
    else pagina=3;
    desenharPagina=true;
  } else if (y>=155 && y<=187) {
    if (pagina==1) {
      if(x<160) ajustarModoLuz(0);
      else ajustarModoLuz(luzLigada ? 1 : 2);
    } else if (pagina==2) moverPortao(x<160 ? ABERTO : FECHADO,false);
    else if (pagina==3) {
      if(x<160) ajustarModoBomba(0);
      else ajustarModoBomba((bombaLigada || modoBomba==2) ? 1 : 2);
    } else if (pagina==4) {
      if(x<160) alternarTesteAlarme();
      else cancelarAlarme();
    }
  }
}

void lerToque() {
  unsigned long agora=millis();
  if (agora-consultaToque<20) return;
  consultaToque=agora;
  TSPoint p=toque.getPoint();
  // Restaura os pinos compartilhados com o barramento paralelo do TFT.
  pinMode(XM,OUTPUT);
  pinMode(YP,OUTPUT);
  bool valido=p.z>=PRESSAO_MIN && p.z<=PRESSAO_MAX;
  if (valido) {
    ultimoContato=agora;
    if (!toqueTravado) {
      toqueTravado=true;
      int x=map(p.y,TS_TOP,TS_BOT,0,319);
      int y=map(p.x,TS_RT,TS_LEFT,0,239);
      // Ignora leituras claramente fora da calibracao; nao prende nas bordas.
      if (x>=-10 && x<=329 && y>=-10 && y<=249)
        tratarToque(constrain(x,0,319),constrain(y,0,239));
    }
  } else if (agora-ultimoContato>=90) toqueTravado=false;
}

void atualizarTela() {
  unsigned long agora=millis();
  if(avisoDHTAtivo) {
    if((long)(agora-fimAvisoDHT)<0) {
      if(!avisoDHTDesenhado) {
        tela.fillRect(4,36,312,44,PAINEL);
        tela.drawRect(4,36,312,44,VERMELHO);
        texto(12,41,"DHT SEM LEITURA",2,VERMELHO);
        texto(12,64,"Verifique o sensor e as conexoes.",1,BRANCO);
        avisoDHTDesenhado=true;
      }
      return;
    }
    avisoDHTAtivo=false;avisoDHTDesenhado=false;
    desenharPagina=true;
  }
  if(atualizarCabecalho) {
    tela.fillRoundRect(257,5,56,22,5,apresentacao ? VERDE : AZUL);
    centralizar(257,12,56,apresentacao ? "AUTO" : "PAUSA",1,
                apresentacao ? FUNDO : BRANCO);
    atualizarCabecalho=false;
  }
  // O giro permite apenas animacao incremental e mudanca explicita de pagina.
  // A posicao do motor usa tempo decorrido e nao depende do numero de quadros.
  if(movendo) {
    if(desenharPagina) {
      desenharBase();desenharConteudo();ultimaUI=millis();
    }
    animarPagina();
    return;
  }
  if(apresentacao && agora-ultimaTroca>=TROCA_PAGINA && !toqueTravado)
    mudarPagina(1,false);
  if(desenharPagina) {
    desenharBase();desenharConteudo();ultimaUI=millis();
  } else if(agora-ultimaUI>=250) {
    ultimaUI=agora;desenharConteudo();
  }
  desenharRelogio();
  animarPagina();
}

void mensagensSerial() {
  if(movendo) return; // Evita encher o buffer Serial durante o movimento.
  unsigned long agora=millis();
  if(agora-msgBoia>=500) {
    msgBoia=agora;
    Serial.print(F("[BOIA] ")); Serial.print(digitalRead(P_BOIA));
    Serial.print(F(" | Comando bomba: ")); Serial.println(bombaLigada ? F("ON") : F("OFF"));
  }
  if(agora-msgSensores>=30000) {
    msgSensores=agora;
    Serial.print(F("[DHT] ")); Serial.print(temperatura,1);
    Serial.print(F(" C | ")); Serial.print(umidade,1); Serial.println(F(" %"));
    Serial.print(F("[HIGRO A8] ")); Serial.println(higro);
    Serial.print(F("[LDR A9] ")); Serial.println(ldr);
  }
}

void aberturaVisual() {
  tela.fillScreen(FUNDO);
  for(int y=0;y<240;y+=3) tela.fillRect(0,y,320,3,tela.color565(5,12+y/12,24+y/5));
  desenhoCasa(142,38,CIANO);
  centralizar(0,93,320,"NEXUS",4,BRANCO);
  centralizar(0,139,320,"CASA INTELIGENTE",2,CIANO);
  centralizar(0,168,320,"Controle integrado",1,TEXTO);
  tela.drawRoundRect(49,194,222,12,5,BORDA);
  for(int w=0;w<=214;w+=7) {
    tela.fillRoundRect(53,198,w,4,2,CIANO);
    delay(12); // Somente na abertura; bomba mantida desligada.
  }
}

void setup() {
  digitalWrite(P_RELE,RELE_OFF); pinMode(P_RELE,OUTPUT);
  digitalWrite(P_LUZ,LUZ_OFF); pinMode(P_LUZ,OUTPUT);
  const byte leds[]={P_LED_PORTAO,P_LED_ALARME,P_LED_AGUA,P_BUZZER};
  for(byte i=0;i<sizeof(leds);i++) {digitalWrite(leds[i],LOW); pinMode(leds[i],OUTPUT);}
  for(byte i=0;i<sizeof(botoes);i++) pinMode(botoes[i],INPUT_PULLUP);
  pinMode(P_BOIA,INPUT_PULLUP);
  pinMode(P_HIGRO,INPUT); pinMode(P_LDR,INPUT);
  Serial.begin(9600);
  iniciarRelogio();
  dht.begin();
  // Controlador 0x9341 confirmado nos testes anteriores deste display.
  tela.begin(0x9341);
  tela.setRotation(1);
  tela.setTextWrap(false);
  aberturaVisual();
  SPI.begin();
  inicializarRFID();
  portao.write(FECHADO);
  portao.attach(P_SERVO);
  boiaAnterior=digitalRead(P_BOIA);
  mudouBoia=millis();
  ultimaTroca=millis();
  Serial.println(F("NEXUS TFT INTEGRADO R06"));
  Serial.println(F("Relogio por software. Ajuste: H AAAA-MM-DD HH:MM:SS (Nova linha)"));
  Serial.println(F("Servo30 Botao32 LED33 | LDR A9 LED34 | Higro A8 LED28"));
  Serial.println(F("Anterior25 Proxima26 | Boia43 Rele42 | DHT22 Buzzer44"));
  Serial.println(rfidOK ? F("[RFID] Pronto") : F("[RFID] Falha: tentara novamente"));
  notificar("Toque ou use os botoes para navegar");
}

void loop() {
  atualizarRelogio();
  lerAjusteRelogio();
  atualizarBomba();
  lerBotoes();
  atualizarPortao();
  lerToque();
  atualizarRFID();
  atualizarPortao();
  atualizarAnalogicos();
  atualizarTemperatura();
  atualizarAlarme();
  atualizarBomba();
  atualizarTela();
  atualizarPortao();
  atualizarBomba();
  mensagensSerial();
}
