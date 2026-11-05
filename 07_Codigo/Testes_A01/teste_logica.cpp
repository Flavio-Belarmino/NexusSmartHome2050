// Testes da decisao de controle. Nao simulam a fisica dos sensores.
#include "../NEXUS_A01_Bancada/controle_luz.h"
#include <assert.h>
#include <stdio.h>

int main() {
  using namespace nexus;
  ConfigLuz cfg = {1000, 5000, 20, 80};
  ControleLuz c(cfg, 0);
  assert(!c.atualizar(0, 100, true));
  c.modo(Modo::Automatico);
  assert(!c.atualizar(2000, 100, true));  // bloqueio sem calibracao
  assert(!c.calibrar(500, 530));  // faixa insuficiente
  assert(!c.calibrar(-1, 100));
  assert(!c.calibrar(800, 1024));
  assert(c.calibrar(800, 200));
  assert(!c.atualizar(999, 200, true));  // estabilizacao
  assert(!c.atualizar(1000, 800, true));  // claro com movimento
  assert(c.atualizar(1100, 200, true));
  assert(c.atualizar(6000, 500, false));  // histerese e permanencia
  assert(!c.atualizar(6100, 500, false));  // expira na fronteira exata
  assert(c.atualizar(6200, 200, true));
  assert(!c.atualizar(6300, 800, true));  // iluminar desliga
  c.modo(Modo::Ligado);
  assert(c.atualizar(6301, 800, false));
  c.modo(Modo::Desligado);
  assert(!c.atualizar(6302, 200, true));
  c.modo(Modo::Automatico);
  assert(!c.atualizar(6303, 200, false));  // nao usa movimento antigo
  assert(c.calibrar(200, 800));  // polaridade inversa
  assert(c.atualizar(6400, 800, true));
  assert(c.atualizar(11400, 800, true));  // HIGH prolongado renova tempo
  assert(c.atualizar(16399, 500, false));
  assert(!c.atualizar(16400, 500, false));
  assert(!c.atualizar(16401, -1, true));
  assert(!c.calibrar(500, 500));
  assert(!c.atualizar(17000, 800, true));

  ConfigLuz rapida = {0, 100, 20, 80};
  const uint32_t inicio = 0xFFFFFFF0UL;
  ControleLuz rollover(rapida, inicio);
  assert(rollover.calibrar(800, 200));
  rollover.modo(Modo::Automatico);
  assert(rollover.atualizar(inicio, 200, true));
  assert(rollover.atualizar(static_cast<uint32_t>(inicio + 99), 200, false));
  assert(!rollover.atualizar(static_cast<uint32_t>(inicio + 100), 200, false));
  puts("OK: 28 verificacoes da logica A01; sem validacao fisica dos sensores.");
  return 0;
}
