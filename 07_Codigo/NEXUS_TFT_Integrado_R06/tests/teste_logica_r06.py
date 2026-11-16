from pathlib import Path
import subprocess

import tempfile
work=tempfile.TemporaryDirectory(prefix='nexus_r06_')
base=Path(work.name)
src=(Path(__file__).resolve().parent.parent/'NEXUS_TFT_Integrado_R06.ino').read_text()
stub=r'''
#include <cstdio>
#include <algorithm>
#include <cstring>
#include <cmath>
#include <cstdint>
#include <cassert>
#include <iostream>
#include <string>
using byte=uint8_t;
using std::min;using std::max;
int toneFreq=0,screenClears=0,fillPixels=0;
using std::isnan;
#define HIGH 1
#define LOW 0
#define INPUT 0
#define OUTPUT 1
#define INPUT_PULLUP 2
#define A0 54
#define A1 55
#define A2 56
#define A3 57
#define A4 58
#define A8 62
#define A9 63
#define DHT22 22
#define F(x) x
unsigned long clockNow=0;
int pins[80]={0}, adc[80]={0};
unsigned long millis(){return clockNow;}
void delay(unsigned long n){clockNow+=n;}
void pinMode(byte,int){}
void digitalWrite(byte p,int v){pins[p]=v;}
int digitalRead(byte p){return pins[p];}
int analogRead(byte p){return adc[p];}
void tone(byte,int hz){toneFreq=hz;}
void noTone(byte){toneFreq=0;}
long map(long x,long a,long b,long c,long d){return (x-a)*(d-c)/(b-a)+c;}
template<class T> T constrain(T x,T a,T b){return x<a?a:(x>b?b:x);}
char* dtostrf(double n,signed char w,unsigned char p,char* s){sprintf(s,"%*.*f",w,p,n);return s;}
struct SerialClass {int available(){return 0;}int read(){return -1;}void begin(int){} template<class... T> void print(T...){} template<class... T> void println(T...){} } Serial;
struct SPIClass {void begin(){}} SPI;
struct Servo {int last=0;void write(int n){last=n;}void attach(byte){}};
struct DHT {float t=24,h=70;DHT(byte,int){}void begin(){}float readTemperature(){return t;}float readHumidity(){return h;}};
struct MFRC522 {
 enum {VersionReg=0}; struct {byte size=4;byte uidByte[10]={0};} uid;
 bool present=false;
 MFRC522(byte,byte){}void PCD_Init(){}byte PCD_ReadRegister(int){return 0x92;}
 bool PICC_IsNewCardPresent(){return present;}bool PICC_ReadCardSerial(){return present;}
 void PICC_HaltA(){present=false;}void PCD_StopCrypto1(){}
};
struct TSPoint {int x=0,y=0,z=0;};
struct TouchScreen {TSPoint p;TouchScreen(int,int,int,int,int){}TSPoint getPoint(){return p;}};
struct MCUFRIEND_kbv {
 template<class... T> void setTextSize(T...){} template<class... T> void setTextColor(T...){}
 template<class... T> void setCursor(T...){} template<class... T> void print(T...){}
 template<class... T> void fillRoundRect(T...){} template<class... T> void drawRoundRect(T...){}
 void fillRect(int,int,int w,int h,uint16_t){fillPixels+=w*h;} template<class... T> void drawRect(T...){}
 template<class... T> void fillCircle(T...){} template<class... T> void drawCircle(T...){}
 template<class... T> void drawLine(T...){} template<class... T> void drawFastHLine(T...){}
 template<class... T> void drawPixel(T...){} template<class... T> void fillScreen(T...){screenClears++;}
 void begin(int){}void setRotation(int){}void setTextWrap(bool){}
 uint16_t color565(int r,int g,int b){return ((r&248)<<8)|((g&252)<<3)|(b>>3);}
};
'''
body='\n'.join(l for l in src.splitlines() if not l.startswith('#include'))
tests=r'''
int main(){
 for(int &p:pins)p=HIGH;
 // Pump: start full; low enables, high overrides immediately.
 boiaAnterior=boiaEstavel=HIGH;boiaValida=false;mudouBoia=0;clockNow=300;
 atualizarBomba();assert(!bombaLigada && pins[P_RELE]==RELE_OFF);
 pins[P_BOIA]=LOW;clockNow=400;atualizarBomba();assert(!bombaLigada);
 clockNow=601;atualizarBomba();assert(bombaLigada && pins[P_RELE]==RELE_ON);
 ajustarModoBomba(1);assert(!bombaLigada);
 ajustarModoBomba(2);assert(bombaLigada);
 pins[P_BOIA]=HIGH;clockNow=602;atualizarBomba();assert(!bombaLigada);
 ajustarModoBomba(2);assert(!bombaLigada && pins[P_RELE]==RELE_OFF);
 clockNow=900;atualizarBomba();assert(!bombaLigada);
 // Water hysteresis and the confirmed inverted LDR output.
 adc[P_HIGRO]=722;adc[P_LDR]=194;clockNow=1100;atualizarAnalogicos();
 assert(vazamento && pins[P_LED_AGUA]==HIGH && pins[P_LUZ]==LOW);
 adc[P_HIGRO]=850;clockNow=1201;atualizarAnalogicos();assert(vazamento);
 adc[P_HIGRO]=1020;adc[P_LDR]=700;clockNow=1302;atualizarAnalogicos();
 assert(!vazamento && pins[P_LED_AGUA]==LOW && pins[P_LUZ]==HIGH);
 // Alarm cancellation persists while hot, then rearms after cooling.
 clockNow=4000;movendo=false;dht.t=30.2;atualizarTemperatura();assert(quente && faseAlarme);
 cancelarAlarme();assert(alarmeCancelado && !faseAlarme);
 clockNow=6600;atualizarTemperatura();assert(alarmeCancelado && !faseAlarme);
 dht.t=29.4;clockNow=9200;atualizarTemperatura();assert(!quente && !alarmeCancelado);
 dht.t=30.1;clockNow=11800;atualizarTemperatura();assert(quente && !alarmeCancelado);
 // Servo speed matches the bench test; manual opening stays open.
 assert(PASSO_SERVO==10 && ABERTO-FECHADO==90 && ESPERA_PORTAO==3000);
 posicao=destino=FECHADO;movendo=false;clockNow=12000;moverPortao(ABERTO,false);
 for(int i=0;i<90;i++){clockNow+=10;atualizarPortao();}
 clockNow+=251;atualizarPortao();assert(!movendo && posicao==90 && !esperandoFechar);
 clockNow+=4000;atualizarPortao();assert(destino==ABERTO);
 // Authorized RFID closes an already opened door.
 rfidOK=true;memcpy(rfid.uid.uidByte,UID1,4);rfid.present=true;
 atualizarRFID();assert(destino==FECHADO && movendo && !fecharDepois);
 for(int i=0;i<90;i++){clockNow+=10;atualizarPortao();}
 clockNow+=251;atualizarPortao();assert(posicao==0 && !movendo);
 // Other authorized UID opens and returns after 3s fully open.
 memcpy(rfid.uid.uidByte,UID2,4);rfid.present=true;clockNow+=100;atualizarRFID();
 assert(destino==ABERTO && fecharDepois);
 for(int i=0;i<90;i++){clockNow+=10;atualizarPortao();}
 clockNow+=251;atualizarPortao();assert(esperandoFechar);
 clockNow+=2999;atualizarPortao();assert(destino==ABERTO);
 clockNow+=1;atualizarPortao();assert(destino==FECHADO && movendo);
 // Unknown UID cannot command another move.
 memset(rfid.uid.uidByte,0,4);rfid.present=true;clockNow+=100;atualizarRFID();assert(destino==FECHADO);
 // Navigation wraps; manual navigation pauses automatic presentation.
 pagina=0;apresentacao=true;mudarPagina(-1,true);assert(pagina==4 && !apresentacao);
 mudarPagina(1,true);assert(pagina==0);
 tratarToque(280,12);assert(apresentacao);
 tratarToque(280,220);assert(!apresentacao && pagina==1);
 // The calibrated center maps inside the display.
 int x=map(575,TS_TOP,TS_BOT,0,319),y=map(563,TS_RT,TS_LEFT,0,239);
 assert(x>140 && x<180 && y>100 && y<140);
 // Render every page through the actual drawing functions.
 for(pagina=0;pagina<5;pagina++){desenharBase();desenharConteudo();animarPagina();}

 // Time-based movement recovers steps missed during a slow loop.
 movendo=false;posicao=destino=FECHADO;clockNow=100000;
 moverPortao(ABERTO,false);
 clockNow+=57;atualizarPortao();assert(posicao==5);
 clockNow+=843;atualizarPortao();assert(posicao==90 && movendo);
 clockNow+=250;atualizarPortao();assert(!movendo);
 moverPortao(FECHADO,false);
 clockNow+=450;atualizarPortao();assert(posicao==45);
 // Reverse partway without resetting to either end.
 moverPortao(ABERTO,false);
 clockNow+=450;atualizarPortao();assert(posicao==90);
 clockNow+=250;atualizarPortao();assert(!movendo);
 // Display painting is deferred while moving, sensor routines remain separate.
 moverPortao(FECHADO,false);desenharPagina=true;
 atualizarTela();assert(!desenharPagina);
 clockNow+=900;atualizarPortao();clockNow+=250;atualizarPortao();
 atualizarTela();assert(!desenharPagina);
 // Clock handles midnight, leap days, year boundary and invalid dates.
 assert(ajustarRelogio("H 2026-11-15 23:59:59"));
 clockNow+=1000;atualizarRelogio();
 assert(anoRelogio==2026 && mesRelogio==11 && diaRelogio==16 && segundosDoDia==0);
 assert(ajustarRelogio("H 2028-02-28 23:59:59"));
 clockNow+=1000;atualizarRelogio();assert(diaRelogio==29 && mesRelogio==2);
 clockNow+=86400000UL;atualizarRelogio();assert(diaRelogio==1 && mesRelogio==3);
 assert(ajustarRelogio("H 2026-12-31 23:59:59"));
 clockNow+=1000;atualizarRelogio();assert(anoRelogio==2027 && mesRelogio==1 && diaRelogio==1);
 assert(!ajustarRelogio("H 2026-02-29 12:00:00"));
 assert(!ajustarRelogio("H 2026-11-15 24:00:00"));
 assert(!ajustarRelogio("H 2026-11-15 20:30:00 extra"));
 pagina=0;segundoDesenhado=86400;desenharRelogio();assert(segundoDesenhado==segundosDoDia);

 // Gate visuals progress slowly even while physical servo movement runs.
 apresentacao=false;avisoDHTAtivo=false;movendo=true;
 pagina=2;anguloVisual=0;destino=ABERTO;desenharPagina=true;
 atualizarTela();int visualAntes=anguloVisual;
 screenClears=0;fillPixels=0;
 clockNow+=80;atualizarTela();
 assert(anguloVisual>visualAntes && anguloVisual<=4 && screenClears==0);
 assert(fillPixels<1000); // Incremental update, not full frame clearing.
 movendo=false;
 for(int i=0;i<50;i++){clockNow+=80;animarPagina();}
 assert(anguloVisual==ABERTO);
 destino=FECHADO;clockNow+=80;animarPagina();assert(anguloVisual==88);
 // Water rises gradually, capped below full until the float reports full.
 pagina=3;desenharBase();nivelVisual=0;bombaLigada=true;boiaValida=true;boiaEstavel=LOW;
 clockNow+=160;animarPagina();assert(nivelVisual==1);
 for(int i=0;i<100;i++){clockNow+=160;animarPagina();}
 assert(nivelVisual==85);
 boiaEstavel=HIGH;bombaLigada=false;
 for(int i=0;i<10;i++){clockNow+=160;animarPagina();}
 assert(nivelVisual==100);
 // LDR icon represents ambient state, independent of manual lamp command.
 pagina=1;desenharBase();escuro=true;desenharAstro();assert(ultimaLua==1);
 escuro=false;desenharAstro();assert(ultimaLua==0);
 assert(corTemperatura(18)==AZUL && corTemperatura(30)==VERMELHO);
 assert(corTemperatura(24)!=AZUL && corTemperatura(24)!=VERMELHO);
 // Original beep alternates 250 ms on/off, synchronized with the LED.
 quente=true;alarmeCancelado=false;faseAlarme=true;piscaAlarme=clockNow;
 saidasAlarme();assert(toneFreq==2000 && pins[P_LED_ALARME]==HIGH);
 clockNow+=249;atualizarAlarme();assert(toneFreq==2000);
 clockNow+=1;atualizarAlarme();assert(toneFreq==0 && pins[P_LED_ALARME]==LOW);
 clockNow+=250;atualizarAlarme();assert(toneFreq==2000 && pins[P_LED_ALARME]==HIGH);
 cancelarAlarme();assert(toneFreq==0 && pins[P_LED_ALARME]==LOW);
 clockNow+=1000;atualizarAlarme();assert(toneFreq==0);
 // Global DHT notice is shown on every page, expires, and does not spam.
 movendo=false;falhaDHTAvisada=false;dht.t=NAN;clockNow+=2600;
 atualizarTemperatura();assert(avisoDHTAtivo && falhaDHTAvisada);
 for(pagina=0;pagina<5;pagina++) {
   avisoDHTDesenhado=false;atualizarTela();assert(avisoDHTDesenhado);
 }
 pagina=0;clockNow+=3001;atualizarTela();assert(!avisoDHTAtivo);
 atualizarTemperatura();assert(!avisoDHTAtivo);
 dht.t=24;clockNow+=2600;atualizarTemperatura();assert(!falhaDHTAvisada);
 dht.t=NAN;clockNow+=2600;atualizarTemperatura();assert(avisoDHTAtivo);

 // Touch test works cold, runs for 3 seconds, never changes actual temperature.
 avisoDHTAtivo=false;quente=false;alarmeCancelado=false;testeAlarme=false;
 temperatura=24;pagina=4;
 tratarToque(50,170);assert(testeAlarme && toneFreq==2000 && !quente && temperatura==24);
 clockNow+=250;atualizarAlarme();assert(toneFreq==0 && testeAlarme);
 clockNow+=250;atualizarAlarme();assert(toneFreq==2000);
 clockNow+=2500;atualizarAlarme();assert(!testeAlarme && toneFreq==0);
 // Onscreen SILENCIAR and the same function used by physical button both stop test.
 tratarToque(50,170);tratarToque(220,170);assert(!testeAlarme && toneFreq==0);
 alternarTesteAlarme();cancelarAlarme();assert(!testeAlarme && toneFreq==0);
 // A test ending must never cancel a real hot alarm.
 quente=true;alarmeCancelado=false;alternarTesteAlarme();
 clockNow+=3000;atualizarAlarme();assert(!testeAlarme && quente && !alarmeCancelado);
 cancelarAlarme();assert(alarmeCancelado && toneFreq==0);
 // Test on a silenced hot alarm does not rearm the actual alarm.
 alternarTesteAlarme();clockNow+=3000;atualizarAlarme();
 assert(!testeAlarme && quente && alarmeCancelado && toneFreq==0);
 std::cout<<"PASS: TFT alarm test/timeout/silence/thermal independence, slow incremental gate/water visuals, LDR icons, temperature colors, original intermittent beep/cancel, global DHT warning/recovery, elapsed-time servo, clock/calendar validation, pump interlock, sensor thresholds, alarm reset, gate manual/RFID/timer, navigation, calibration, drawing paths.\n";
}
'''
test=base/'test_logic.cpp'
test.write_text(stub+body+tests)
subprocess.run(['g++','-std=c++11','-O2',str(test),'-o',str(base/'test_logic')],check=True)
subprocess.run([str(base/'test_logic')],check=True)

work.cleanup()
