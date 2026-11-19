/* NEXUS / DISPLAY DEMO v1.0, 18/11/2026
 * SOMENTE demonstracao: nenhuma leitura de sensor ou comando de atuador.
 * Shield UNO paralelo 8 bits, ILI9486, 480x320, no Mega 2560.
 * Bibliotecas: MCUFRIEND_kbv, Adafruit GFX, Adafruit TouchScreen.
 * Sem SD, sem imagens externas, sem framebuffer, sem String dinamica.
 * EEPROM 0..sizeof(Calibration)-1 reservada para calibracao deste ensaio.
 */
#include "NexusDisplay.h"
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <EEPROM.h>
#include <math.h>

// Deixe 0 para ler o ID. Somente IDs ilegiveis usam 0x9486 como alternativa.
// Se a placa entregue tiver outro controlador, confirme antes de alterar.
#ifndef NEXUS_FORCE_ID
#define NEXUS_FORCE_ID 0
#endif
static const uint8_t ROTATION = 1;
static const uint16_t W=480, H=320;
static const uint16_t BG=0x0843, PANEL=0x10C7, WHITE=0xFFFF, MUTED=0x9D15;
static const uint16_t CYAN=0x07FF, GREEN=0x07EA, PURPLE=0xA81F;
static const uint16_t AMBER=0xFE60, RED=0xF928, BLUE=0x249F;
static MCUFRIEND_kbv tft;
// Valores comuns no shield 3.5; a descoberta abaixo tenta os pares reais.
static uint8_t xp=8, yp=A3, xm=A2, ym=9;
static TouchScreen ts(8,A3,A2,9,300);
static uint16_t readId=0, usedId=0;
static bool fallbackId=false, supportedSize=false;
enum Page : uint8_t { HOME, GATE, LIGHTS, CLIMATE, ENERGY, WATER, ACCESS, ALERTS, TESTS, COLORS };
static Page page=HOME;
static bool automatic=false, calibrated=false, calibrating=false;
static uint32_t lastFrame=0, pageSince=0, lastTouch=0;
static uint16_t phase=0;
static uint8_t rooms=5, rgb=0, accessState=0;
static bool alarmOn=false, rain=false, gas=false, flame=false, pump=false, leak=false;
static int gatePos=0, gateTarget=0;
static uint32_t accessSince=0;
static const uint16_t rgbColors[]={CYAN,PURPLE,AMBER,GREEN,RED,BLUE};
static uint32_t frameInterval=140;
// Transformacao afim: x=a*rawX+b*rawY+c; y=d*rawX+e*rawY+f.
struct Calibration {
  uint32_t magic;
  uint8_t version, rotation, pins[4];
  float a,b,c,d,e,f;
  uint16_t checksum;
};
static Calibration cal;
static const uint32_t CAL_MAGIC=0x4E583335UL;
static uint8_t calStep=0, calCount=0;
static bool calWaitRelease=true;
static uint32_t calStarted=0;
static int32_t sumX=0,sumY=0;
static int16_t rx[4],ry[4],prevRawX=0,prevRawY=0;
static const int16_t targetX[]={24,455,24,455};
static const int16_t targetY[]={24,24,295,295};

static void text(int x,int y,const __FlashStringHelper *s,uint8_t size=2,uint16_t color=WHITE) {
  tft.setTextSize(size); tft.setTextColor(color); tft.setCursor(x,y); tft.print(s);
}
static void number(int x,int y,int value,uint8_t size=2,uint16_t color=WHITE) {
  tft.setTextSize(size); tft.setTextColor(color); tft.setCursor(x,y); tft.print(value);
}
static void box(int x,int y,int w,int h,uint16_t fill=PANEL) {
  tft.fillRoundRect(x,y,w,h,9,fill);
}
static void button(int x,int y,int w,int h,const __FlashStringHelper *s,uint16_t color=CYAN) {
  box(x,y,w,h,color); text(x+10,y+(h-16)/2,s,2,BG);
}
static bool inside(int x,int y,int l,int t,int w,int h) { return x>=l && x<l+w && y>=t && y<t+h; }
static void bulb(int x,int y,bool on,uint16_t color=AMBER) {
  uint16_t c=on?color:MUTED;
  tft.fillCircle(x,y,12,c); tft.fillRect(x-6,y+10,12,8,c);
  tft.drawFastHLine(x-5,y+21,10,c);
  if(on) { for(uint8_t i=0;i<8;i++) {
    float a=i*0.785398f;
    tft.drawLine(x+18*cos(a),y+18*sin(a),x+23*cos(a),y+23*sin(a),c);
  }}
}
static void house(int x,int y,uint16_t color) {
  tft.drawTriangle(x,y,x+25,y-20,x+50,y,color);
  tft.drawRect(x+5,y,40,32,color); tft.fillRect(x+21,y+13,10,19,color);
}
static void drop(int x,int y,uint16_t c) {
  tft.fillTriangle(x,y-18,x-11,y,x+11,y,c);tft.fillCircle(x,y,11,c);
}
static void lockIcon(int x,int y,uint16_t c,bool open=false) {
  tft.drawRoundRect(x-12,y-20,24,28,10,c);
  if(open)tft.fillRect(x+8,y-10,8,15,PANEL);
  tft.fillRoundRect(x-20,y,40,28,5,c);tft.fillCircle(x,y+12,3,BG);
}
static void bell(int x,int y,uint16_t c,bool pulse) {
  tft.fillRoundRect(x-13,y-20,26,31,12,c);tft.fillRect(x-19,y+7,38,5,c);
  tft.fillCircle(x,y+17,4,c);
  if(pulse) {tft.drawCircle(x,y-5,30,c);tft.drawCircle(x,y-5,34,c);}
}
static const __FlashStringHelper *title(Page p) {
  switch(p) {
    case GATE:return F("PORTAO");case LIGHTS:return F("LUZES");case CLIMATE:return F("CLIMA");
    case ENERGY:return F("ENERGIA");case WATER:return F("AGUA");case ACCESS:return F("ACESSO RFID");
    case ALERTS:return F("ALERTAS");case TESTS:return F("TESTES DO DISPLAY");case COLORS:return F("CORES / PIXELS");
    default:return F("NEXUS");
  }
}
static void footer() {
  tft.fillRect(0,280,W,40,BG);
  button(6,284,102,32,F("INICIO"),PURPLE);
  button(114,284,104,32,F("ANTES"),MUTED);
  button(224,284,112,32,automatic?F("PAUSAR"):F("AUTO"),automatic?AMBER:CYAN);
  button(342,284,132,32,F("PROXIMA"),CYAN);
}
static void header() {
  tft.fillScreen(BG);text(14,10,title(page),3,CYAN);
  box(344,8,124,24,PURPLE);text(354,13,F("DEMO"),2);
  text(14,40,F("DADOS SIMULADOS - SEM ACIONAR A MAQUETE"),1,MUTED);
  tft.drawFastHLine(12,54,456,PANEL);footer();
}
static void homeIcon(uint8_t n,int x,int y) {
  switch(n) {
    case 0: house(x-25,y-4,CYAN);break;
    case 1: bulb(x,y,true);break;
    case 2: tft.drawRoundRect(x-7,y-24,14,42,6,CYAN);tft.fillCircle(x,y+16,11,RED);break;
    case 3: tft.drawRect(x-24,y-16,48,32,CYAN);tft.fillCircle(x+30,y-24,8,AMBER);break;
    case 4: drop(x,y,CYAN);break;
    case 5: lockIcon(x,y-8,GREEN);break;
    case 6: bell(x,y,RED,false);break;
    default: tft.drawCircle(x,y,22,PURPLE);text(x-6,y-7,F("+"),2,CYAN);break;
  }
}
static void drawHome() {
  for(uint8_t i=0;i<8;i++) {
    int x=9+(i%4)*118, y=63+(i/4)*105;
    box(x,y,109,97);homeIcon(i,x+54,y+35);
    const __FlashStringHelper *s=i==7?F("TESTES"):title((Page)(i+1));
    // ACESSO cabe no cartao; o titulo completo aparece na pagina.
    if(i==5)s=F("ACESSO");
    text(x+9,y+76,s,2,WHITE);
  }
}
static void drawGateFrame() {
  box(12,64,218,166);
  tft.drawTriangle(28,100,120,70,212,100,CYAN);
  tft.drawRect(35,101,170,113,CYAN);
  int height=map(gatePos,0,100,106,0);
  if(height>0) { tft.fillRect(39,105,162,height,MUTED);
    for(int y=108;y<105+height;y+=11)tft.drawFastHLine(39,y,162,BG); }
  text(246,76,gatePos==gateTarget?(gatePos==0?F("FECHADO"):F("ABERTO")):
      (gateTarget>gatePos?F("ABRINDO"):F("FECHANDO")),2,GREEN);
  text(246,107,F("SIMULACAO"),2,AMBER);
  text(246,134,F("Sem sensor de posicao"),1,MUTED);
  text(246,152,F("Obstaculo: LIVRE"),1,MUTED);
  button(246,180,102,44,F("ABRIR"),GREEN);button(358,180,108,44,F("FECHAR"),AMBER);
  text(18,245,F("Animacao ilustrativa do movimento comandado."),1,MUTED);
}
static void drawLights() {
  const __FlashStringHelper *names[]={F("SALA"),F("QUARTO"),F("COZINHA"),F("GARAGEM")};
  for(uint8_t i=0;i<4;i++) {
    int x=12+(i%2)*125,y=65+(i/2)*93;
    box(x,y,117,85,(rooms&(1<<i))?0x39A3:PANEL);
    bulb(x+58,y+26,rooms&(1<<i),rgbColors[rgb]);text(x+8,y+63,names[i],2);
  }
  text(276,67,F("COR RGB"),2,CYAN);
  tft.fillRect(272,89,198,103,BG);
  for(uint8_t i=0;i<6;i++) {
    int x=278+(i%3)*63,y=94+(i/3)*51;
    box(x,y,51,40,rgbColors[i]);if(i==rgb)tft.drawRoundRect(x-2,y-2,55,44,10,WHITE);
  }
  button(274,203,192,31,F("LIGAR TUDO"),GREEN);
  button(274,241,192,31,F("APAGAR TUDO"),MUTED);
}
static void drawClimate() {
  box(12,65,218,130);box(242,65,226,130);
  text(24,78,F("TEMPERATURA"),2,CYAN);text(256,78,F("UMIDADE"),2,CYAN);
  int v=264+(int)((phase/6)%9)-4;
  number(24,113,v/10,5);text(86,133,F(","),3);number(104,113,abs(v%10),5);
  text(145,128,F("C"),3,AMBER);tft.drawCircle(141,119,3,AMBER);
  number(259,113,58+(phase/20)%4,5);text(334,128,F("%"),3,CYAN);drop(425,141,CYAN);
  box(12,205,456,64);text(24,214,F("HISTORICO ILUSTRATIVO"),1,MUTED);
  for(int i=0;i<60;i++) {
    int y=246+(int)(11*sin((i+phase)*0.22));
    if(i)tft.drawLine(22+(i-1)*7,246+11*sin((i-1+phase)*0.22),22+i*7,y,CYAN);
  }
}
static void bolt(int x,int y,uint16_t c) {
  tft.fillTriangle(x+6,y-16,x-7,y+3,x+3,y+3,c);
  tft.fillTriangle(x-3,y-3,x+7,y-3,x-6,y+16,c);
}
static void drawEnergy() {
  box(12,65,456,147);
  tft.drawRect(30,109,92,55,CYAN);
  for(int i=1;i<4;i++)tft.drawFastVLine(30+i*23,109,55,CYAN);
  tft.drawFastHLine(30,136,92,CYAN);tft.fillCircle(85,87,13,AMBER);
  tft.drawRect(196,112,95,45,WHITE);tft.fillRect(291,124,7,18,WHITE);
  for(int i=0;i<3;i++)tft.fillRect(203+i*28,119,21,31,GREEN);
  house(372,125,CYAN);
  bolt(154,136,(phase%4<2)?CYAN:PANEL);bolt(337,136,(phase%4>=2)?CYAN:PANEL);
  text(41,181,F("SOLAR"),2);text(199,181,F("BATERIA"),2);text(375,181,F("CASA"),2);
  text(20,226,F("12,6 V - EXEMPLO VISUAL"),2,AMBER);
  text(20,255,F("Fluxo ilustrativo; nao comprova carregamento."),1,MUTED);
}
static void drawWater() {
  box(12,65,218,205);tft.drawRoundRect(43,81,150,167,18,CYAN);
  for(int x=47;x<189;x++) {
    int y=156+(int)(5*sin((x+phase*8)*0.09));
    tft.drawFastVLine(x,y,244-y,BLUE);
    tft.drawPixel(x,y,CYAN);
  }
  tft.fillRect(243,65,225,108,BG);
  text(255,76,F("NIVEL: NORMAL"),2,GREEN);
  text(255,112,leak?F("PISO MOLHADO"):F("PISO SECO"),2,leak?RED:GREEN);
  text(255,151,pump?F("BOMBA: ON"):F("BOMBA: OFF"),2,pump?CYAN:MUTED);
  button(249,188,218,35,F("TESTAR BOMBA"),CYAN);
  button(249,233,218,35,F("VAZAMENTO"),leak?RED:AMBER);
}
static void drawAccess() {
  box(12,65,456,155);
  uint16_t c=accessState==0?CYAN:accessState==1?GREEN:RED;
  tft.drawRoundRect(35,94,90,77,8,c);text(48,120,F("RFID"),2,c);
  for(uint8_t i=0;i<3;i++)tft.drawCircle(155,131,12+i*9,(phase%3==i)?c:PANEL);
  lockIcon(215,127,c,accessState==1);
  text(270,91,accessState==0?F("APROXIME"):accessState==1?F("ACESSO"):F("ACESSO"),2,c);
  text(270,121,accessState==0?F("O CARTAO"):accessState==1?F("AUTORIZADO"):F("NEGADO"),2,c);
  text(270,164,F("Leitura simulada"),1,MUTED);
  button(12,233,218,36,F("AUTORIZAR"),GREEN);button(242,233,226,36,F("NEGAR"),RED);
}
static void drawAlerts() {
  const __FlashStringHelper *names[]={F("GAS"),F("CHAMA"),F("CHUVA")};
  bool states[]={gas,flame,rain};
  for(uint8_t i=0;i<3;i++) {
    int x=12+i*154;box(x,65,146,84);
    text(x+10,77,names[i],2,CYAN);
    text(x+10,118,states[i]?F("ALERTA"):F("NORMAL"),2,states[i]?RED:GREEN);
  }
  box(12,160,456,62,alarmOn?RED:PANEL);bell(43,192,WHITE,alarmOn&&(phase%2));
  text(92,181,alarmOn?F("ALARME DE TESTE"):F("SEM ALERTAS"),2);
  button(12,234,218,35,F("TESTAR ALARME"),AMBER);button(242,234,226,35,F("SILENCIAR"),GREEN);
}
static void drawTests() {
  text(16,67,F("Controlador lido: 0x"),2);tft.print(readId,HEX);
  text(16,94,F("Em uso: 0x"),2);tft.print(usedId,HEX);
  text(16,121,F("Touch: "),2);tft.print(calibrated?F("CALIBRADO"):F("NAO CALIBRADO"));
  text(16,151,F("C no Serial recalibra. 0..8 muda de tela."),1,MUTED);
  button(12,178,218,41,F("CALIBRAR TOUCH"),CYAN);
  button(242,178,226,41,F("TESTAR CORES"),AMBER);
  button(12,232,456,36,F("DEMONSTRACAO AUTOMATICA"),GREEN);
}
static void drawColors() {
  const uint16_t colors[]={0xF800,0x07E0,0x001F,0xFFFF,0x07FF,0xF81F,0xFFE0,0};
  for(uint8_t i=0;i<8;i++)tft.fillRect(i*60,62,60,120,colors[i]);
  text(12,190,F("R   G   B  BRANCO CIANO ROXO AMARELO PRETO"),1);
  for(int i=0;i<32;i++)tft.fillRect(12+i*14,213,14,26,tft.color565(i*255/31,i*255/31,i*255/31));
  tft.drawRect(1,1,478,318,WHITE);text(12,252,F("Confira cores, cinzas, bordas e orientacao."),1,MUTED);
}
static void drawPage() {
  header();switch(page) {
    case HOME:drawHome();break;case GATE:drawGateFrame();break;case LIGHTS:drawLights();break;
    case CLIMATE:drawClimate();break;case ENERGY:drawEnergy();break;case WATER:drawWater();break;
    case ACCESS:drawAccess();break;case ALERTS:drawAlerts();break;case TESTS:drawTests();break;case COLORS:drawColors();break;
  }
}
static void go(Page p) {page=p;pageSince=millis();drawPage();}
static void changePage(int direction) {
  int p=(int)page+direction;if(p<0)p=8;if(p>8)p=0;go((Page)p);
}
static void redrawBody() {
  // Somente a area da funcao e redesenhada; cabecalho e navegacao ficam parados.
  // Cada funcao apaga seus paineis antes de desenhar a proxima etapa.
  switch(page) {
    case GATE: tft.fillRect(240,60,240,114,BG);drawGateFrame();break;
    case CLIMATE:drawClimate();break;case ENERGY:drawEnergy();break;case WATER:drawWater();break;
    case ACCESS:drawAccess();break;case ALERTS:drawAlerts();break;default:break;
  }
}
static uint16_t checksum(const Calibration &c) {
  const uint8_t *p=(const uint8_t *)&c;uint16_t h=0x1573;
  for(size_t i=0;i<offsetof(Calibration,checksum);i++)h=(h*31)^p[i];return h;
}
static bool validCal(const Calibration &c) {
  return c.magic==CAL_MAGIC && c.version==1 && c.rotation==ROTATION &&
    c.pins[0]==xp && c.pins[1]==yp && c.pins[2]==xm && c.pins[3]==ym &&
    c.checksum==checksum(c) && isfinite(c.a) && isfinite(c.b) && isfinite(c.c) &&
    isfinite(c.d) && isfinite(c.e) && isfinite(c.f) && fabs(c.a*c.e-c.b*c.d)>0.01;
}
static TSPoint readRaw() {
  TSPoint p=ts.getPoint();
  // Os pinos do touch sao compartilhados com os sinais do TFT.
  pinMode(xm,OUTPUT);pinMode(yp,OUTPUT);pinMode(xp,OUTPUT);pinMode(ym,OUTPUT);
  return p;
}
static bool pressureOK(const TSPoint &p) {return p.z>20 && p.z<1000 && p.x>5 && p.x<1018 && p.y>5 && p.y<1018;}
static void pixelFromRaw(int rawX,int rawY,int &x,int &y) {
  x=lround(cal.a*rawX+cal.b*rawY+cal.c);y=lround(cal.d*rawX+cal.e*rawY+cal.f);
}
static void calTarget() {
  tft.fillScreen(BG);text(87,91,F("CALIBRAR TOQUE"),3,CYAN);
  text(73,134,F("Segure a caneta no alvo."),2);
  text(87,164,F("Solte entre os pontos."),2);
  text(110,199,F("Ponto "),2);number(182,199,calStep+1);text(207,199,F("de 4"),2);
  text(62,235,F("Sem toque por 30 s: abre demo."),2,MUTED);
  text(84,261,F("Serial: C tenta novamente."),2,MUTED);
  int x=targetX[calStep],y=targetY[calStep];
  tft.drawCircle(x,y,13,CYAN);tft.drawLine(x-18,y,x+18,y,WHITE);tft.drawLine(x,y-18,x,y+18,WHITE);
}
static void startCal() {
  automatic=false;calibrating=true;calStep=calCount=0;sumX=sumY=0;
  calWaitRelease=true;calStarted=millis();calTarget();
  Serial.println(F("Calibracao: toque 4 alvos com a caneta; solte entre eles."));
}
static bool fitCalibration() {
  float ux=rx[1]-rx[0],uy=ry[1]-ry[0],vx=rx[2]-rx[0],vy=ry[2]-ry[0];
  float det=ux*vy-uy*vx;if(fabs(det)<40000)return false;
  memset(&cal,0,sizeof(cal));cal.magic=CAL_MAGIC;cal.version=1;cal.rotation=ROTATION;
  cal.pins[0]=xp;cal.pins[1]=yp;cal.pins[2]=xm;cal.pins[3]=ym;
  cal.a=431*vy/det;cal.b=-431*vx/det;cal.c=24-cal.a*rx[0]-cal.b*ry[0];
  cal.d=-271*uy/det;cal.e=271*ux/det;cal.f=24-cal.d*rx[0]-cal.e*ry[0];
  int x,y;pixelFromRaw(rx[3],ry[3],x,y);
  if(abs(x-455)>22 || abs(y-295)>22)return false;
  cal.checksum=checksum(cal);return validCal(cal);
}
static void calibrationTick() {
  if(millis()-calStarted>30000) {
    calibrating=false;automatic=true;Serial.println(F("Sem calibracao: demo automatica; C repete."));go(HOME);return;
  }
  TSPoint p=readRaw();bool down=pressureOK(p);
  if(calWaitRelease) {if(!down)calWaitRelease=false;return;}
  if(!down) {calCount=0;sumX=sumY=0;return;}
  calStarted=millis();
  if(calCount && (abs(p.x-prevRawX)>18 || abs(p.y-prevRawY)>18)) {calCount=0;sumX=sumY=0;}
  prevRawX=p.x;prevRawY=p.y;sumX+=p.x;sumY+=p.y;
  if(++calCount<12)return;
  rx[calStep]=sumX/calCount;ry[calStep]=sumY/calCount;
  Serial.print(F("Alvo "));Serial.print(calStep+1);Serial.print(F(": "));Serial.print(rx[calStep]);Serial.print(',');Serial.println(ry[calStep]);
  calCount=0;sumX=sumY=0;calWaitRelease=true;
  if(++calStep<4){calTarget();return;}
  if(fitCalibration()) {
    EEPROM.put(0,cal);calibrated=true;calibrating=false;
    Serial.println(F("Touch calibrado e salvo na EEPROM."));go(HOME);
  } else {
    calibrated=false;Serial.println(F("Alvos inconsistentes: repetindo calibracao."));startCal();
  }
}
static void discoverPins() {
  // Mesmo principio do exemplo diagnose_Touchpins da MCUFRIEND_kbv.
  // Executar apenas com o shield sozinho: altera D2..9 e A0..A4.
  uint8_t ap[2]={0,0},dp[2]={0,0};int values[2]={0,0};uint8_t count=0;
  for(int a=A0;a<=A4;a++)pinMode(a,INPUT_PULLUP);
  for(int d=2;d<=9;d++)pinMode(d,INPUT_PULLUP);
  for(int a=A0;a<A4;a++)for(int d=5;d<10;d++) {
    pinMode(d,OUTPUT);digitalWrite(d,LOW);analogRead(a);int v=analogRead(a);
    if(v>0 && v<100) {if(count<2){ap[count]=a;dp[count]=d;values[count]=v;}count++;}
    pinMode(d,INPUT_PULLUP);
  }
  if(count==2 && ap[0]!=ap[1] && dp[0]!=dp[1]) {
    int i=values[0]<values[1]?0:1;xm=ap[i];xp=dp[i];yp=ap[1-i];ym=dp[1-i];
    Serial.println(F("Pares resistivos do touch detectados."));
  } else Serial.println(F("Touch: pares inconclusivos; usando XP8 YP A3 XM A2 YM9."));
  for(int a=A0;a<=A4;a++)pinMode(a,INPUT);
  for(int d=2;d<=9;d++)pinMode(d,INPUT);
  ts=TouchScreen(xp,yp,xm,ym,300);
  Serial.print(F("XP="));Serial.print(xp);Serial.print(F(" YP="));Serial.print(yp);
  Serial.print(F(" XM="));Serial.print(xm);Serial.print(F(" YM="));Serial.println(ym);
}
static void handleTap(int x,int y) {
  // Navegacao so responde ao primeiro toque; caneta mantida nao repete.
  if(y>=284) {
    if(x<110)go(HOME);else if(x<220)changePage(-1);
    else if(x<340){automatic=!automatic;pageSince=millis();footer();}
    else changePage(1);return;
  }
  if(page==HOME) {
    for(uint8_t i=0;i<8;i++)if(inside(x,y,9+i%4*118,63+i/4*105,109,97)){go((Page)(i+1));return;}
  } else if(page==GATE) {
    if(inside(x,y,246,180,102,44))gateTarget=100;
    if(inside(x,y,358,180,108,44))gateTarget=0;
    drawGateFrame();
  } else if(page==LIGHTS) {
    for(uint8_t i=0;i<4;i++)if(inside(x,y,12+i%2*125,65+i/2*93,117,85))rooms^=1<<i;
    for(uint8_t i=0;i<6;i++)if(inside(x,y,278+i%3*63,94+i/3*51,51,40))rgb=i;
    if(inside(x,y,274,203,192,31))rooms=15;if(inside(x,y,274,241,192,31))rooms=0;drawLights();
  } else if(page==WATER) {
    if(inside(x,y,249,188,218,35))pump=!pump;
    if(inside(x,y,249,233,218,35))leak=!leak;drawWater();
  } else if(page==ACCESS) {
    if(y>=233&&y<269) {accessState=x<236?1:2;accessSince=millis();drawAccess();}
  } else if(page==ALERTS) {
    if(y>=65&&y<149) {if(x<164)gas=!gas;else if(x<318)flame=!flame;else rain=!rain;alarmOn=gas||flame||rain;}
    if(inside(x,y,12,234,218,35))alarmOn=true;
    if(inside(x,y,242,234,226,35)){alarmOn=gas=flame=rain=false;}drawAlerts();
  } else if(page==TESTS) {
    if(inside(x,y,12,178,218,41))startCal();
    else if(inside(x,y,242,178,226,41))go(COLORS);
    else if(inside(x,y,12,232,456,36)){automatic=true;go(HOME);}
  }
}
static void serialTick() {
  while(Serial.available()) {
    char c=Serial.read();
    if(c=='c'||c=='C'){startCal();return;}
    if(c=='0'||(c>='1'&&c<='8')){calibrating=false;automatic=false;go((Page)(c-'0'));}
    if(c=='a'||c=='A'){calibrating=false;automatic=!automatic;pageSince=millis();drawPage();}
    if(c=='t'||c=='T'){calibrating=false;go(COLORS);}
  }
}
void nexusSetup() {
  Serial.begin(115200);Serial.println(F("NEXUS DISPLAY DEMO v1.0 / Mega2560 / apenas TFT"));
  discoverPins();tft.reset();readId=tft.readID();usedId=NEXUS_FORCE_ID?NEXUS_FORCE_ID:readId;
  if(!NEXUS_FORCE_ID&&(usedId==0xD3D3||usedId==0xFFFF||usedId==0||usedId==0x0101)) {
    usedId=0x9486;fallbackId=true;
  }
  Serial.print(F("ID lido=0x"));Serial.print(readId,HEX);Serial.print(F(" / em uso=0x"));Serial.println(usedId,HEX);
  if(fallbackId)Serial.println(F("ID ilegivel: alternativa ILI9486 do anuncio. Confirmar placa recebida."));
  tft.begin(usedId);tft.setRotation(ROTATION);tft.setTextWrap(false);
  supportedSize=tft.width()==W&&tft.height()==H;
  if(!supportedSize) {
    tft.fillScreen(BG);text(5,10,F("RESOLUCAO DIFERENTE"),2,RED);
    text(5,45,F("Confira ID no Serial 115200."),1);Serial.println(F("Esperado 480x320. Demo interrompida."));return;
  }
  EEPROM.get(0,cal);calibrated=validCal(cal);
  if(calibrated)go(HOME);else startCal();
  Serial.println(F("Serial: 0..8 paginas | A auto | C calibrar | T cores"));
}
void nexusLoop() {
  if(!supportedSize)return;
  serialTick();
  if(calibrating){calibrationTick();return;}
  static bool wasDown=true;
  if(calibrated) {
    TSPoint p=readRaw();bool down=pressureOK(p);
    if(down&&!wasDown&&millis()-lastTouch>180) {
      int x,y;pixelFromRaw(p.x,p.y,x,y);lastTouch=millis();
      if(x>=0&&x<(int)W&&y>=0&&y<(int)H){handleTap(x,y);pageSince=millis();}
    }
    wasDown=down;
  }
  if(millis()-lastFrame>=frameInterval) {
    lastFrame=millis();phase++;
    if(gatePos<gateTarget)gatePos=min(gateTarget,gatePos+5);
    if(gatePos>gateTarget)gatePos=max(gateTarget,gatePos-5);
    if(accessState&&millis()-accessSince>2600)accessState=0;
    redrawBody();
  }
  if(automatic&&millis()-pageSince>=6500) {
    Page next=(Page)(((int)page+1)%8);
    if(next==GATE)gateTarget=gatePos<50?100:0;
    if(next==LIGHTS){rooms=(rooms==15?5:15);rgb=(rgb+1)%6;}
    if(next==ACCESS){accessState=1;accessSince=millis();}
    if(next==ALERTS){alarmOn=true;gas=flame=rain=false;}
    go(next);
  }
}
