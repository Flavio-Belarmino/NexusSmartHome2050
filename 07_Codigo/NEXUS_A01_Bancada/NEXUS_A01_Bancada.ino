/* Casa Inteligente | NEXUS | ExpoTech
 * A01 R01: primeiro ensaio de iluminacao na bancada, Arduino Mega 2560.
 * Um LED individual, PIR e modulo LDR. Alimentacao somente por USB neste ensaio.
 * Pinagem coerente com R02: LED L01 D22, PIR D35, LDR A0.
 * Ler README.md antes de ligar. Esta versao nao controla os outros sistemas.
 */
#include <Arduino.h>
#include "controle_luz.h"

constexpr uint8_t PIN_LED = 22;
constexpr uint8_t PIN_PIR = 35;
constexpr uint8_t PIN_LDR = A0;
constexpr uint32_t AMOSTRA_MS = 50;
constexpr uint32_t RELATORIO_MS = 1000;
// Valores iniciais para o ensaio. Ajustar somente com resultado registrado.
const nexus::ConfigLuz CONFIG = {60000UL, 5000UL, 20, 80};
nexus::ControleLuz luz(CONFIG, 0);
uint32_t ultimaAmostra = 0;
uint32_t ultimoRelatorio = 0;
int bruto = 0;
int filtrado = 0;
int claro = -1;
int escuro = -1;
bool filtroIniciado = false;
bool pir = false;

void ajuda() {
  Serial.println(F("NEXUS A01 R01 | comandos: 1 liga; 0 desliga; a automatico"));
  Serial.println(F("c captura CLARO; e captura ESCURO; s estado; ? ajuda"));
  Serial.println(F("Calibracao e modo se perdem ao reiniciar. Inicia DESLIGADO."));
}

void estado(uint32_t agora) {
  Serial.print(F("ms=")); Serial.print(agora);
  Serial.print(F(" bruto=")); Serial.print(bruto);
  Serial.print(F(" filtrado=")); Serial.print(filtrado);
  Serial.print(F(" PIR=")); Serial.print(pir ? 1 : 0);
  Serial.print(F(" modo="));
  switch (luz.modo()) {
    case nexus::Modo::Desligado: Serial.print(F("DESLIGADO")); break;
    case nexus::Modo::Ligado: Serial.print(F("LIGADO")); break;
    case nexus::Modo::Automatico: Serial.print(F("AUTO")); break;
  }
  Serial.print(F(" pronto=")); Serial.print(luz.pronto(agora) ? 1 : 0);
  Serial.print(F(" calibrado=")); Serial.print(luz.calibrado() ? 1 : 0);
  Serial.print(F(" escuro=")); Serial.print(luz.escuro() ? 1 : 0);
  Serial.print(F(" LED=")); Serial.println(luz.acesa() ? 1 : 0);
}

void processar(char c, uint32_t agora) {
  switch (c) {
    case '1': luz.modo(nexus::Modo::Ligado); break;
    case '0': luz.modo(nexus::Modo::Desligado); break;
    case 'a': case 'A':
      luz.modo(nexus::Modo::Automatico);
      if (!luz.calibrado()) Serial.println(F("AUTO bloqueado: capture c e e."));
      break;
    case 'c': case 'C':
      claro = filtrado; Serial.print(F("CLARO=")); Serial.println(claro); break;
    case 'e': case 'E':
      escuro = filtrado; Serial.print(F("ESCURO=")); Serial.println(escuro); break;
    case 's': case 'S': estado(agora); return;
    case '?': ajuda(); return;
    case '\r': case '\n': case ' ': return;
    default: Serial.println(F("Comando desconhecido. Envie ?")); return;
  }
  if ((c == 'c' || c == 'C' || c == 'e' || c == 'E') && claro >= 0 && escuro >= 0) {
    const bool ok = luz.calibrar(claro, escuro);
    Serial.println(ok ? F("CALIBRACAO ACEITA") : F("CALIBRACAO RECUSADA: aumente a diferenca claro/escuro."));
    if (ok) { Serial.print(F("CENTRO_ADC=")); Serial.println(luz.centro()); }
  }
}

void setup() {
  // Prepara apenas a saida deste ensaio. Nao conectar outros atuadores.
  digitalWrite(PIN_LED, LOW);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_PIR, INPUT);
  pinMode(PIN_LDR, INPUT);
  Serial.begin(115200);
  bruto = analogRead(PIN_LDR);
  filtrado = bruto;
  filtroIniciado = true;
  ajuda();
}

void loop() {
  const uint32_t agora = millis();
  if (static_cast<uint32_t>(agora - ultimaAmostra) >= AMOSTRA_MS) {
    ultimaAmostra = agora;
    bruto = analogRead(PIN_LDR);
    filtrado = filtroIniciado ? (3 * filtrado + bruto) / 4 : bruto;
    filtroIniciado = true;
    pir = digitalRead(PIN_PIR) == HIGH;
  }
  while (Serial.available() > 0) processar(static_cast<char>(Serial.read()), agora);
  digitalWrite(PIN_LED, luz.atualizar(agora, filtrado, pir) ? HIGH : LOW);
  if (static_cast<uint32_t>(agora - ultimoRelatorio) >= RELATORIO_MS) {
    ultimoRelatorio = agora;
    estado(agora);
  }
}
