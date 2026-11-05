#include "../NEXUS_A05_Agua/controle_agua.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
int main(){
  nexus::ControleAgua c;
  assert(!c.atualizar(0,10,false,0));
  assert(!c.calibrar(10,20));
  assert(!c.calibrar(20,19));
  assert(!c.calibrar(1,0));
  assert(!c.calibrar(NAN,10));
  assert(c.calibrar(30,10));
  assert(!c.atualizar(0,20,false,0));
  assert(c.nivelValido());
  assert(c.nivel()==50);
  c.solicitar(true,100);
  assert(c.atualizar(100,20,false,0));
  assert(!c.atualizar(200,29,false,0));
  assert(c.falha());
  assert(!c.atualizar(300,20,false,0));
  c.rearmar();
  assert(!c.atualizar(400,20,false,0));
  c.solicitar(true,500);
  assert(c.atualizar(500,20,true,500));
  c.solicitar(true,4499); // Repetir pedido nao renova prazo de protecao.
  assert(c.atualizar(4499,20,true,500));
  assert(!c.atualizar(4500,20,true,500));
  assert(c.falha());
  c.rearmar();c.solicitar(true,5000);
  assert(c.atualizar(9000,20,true,8500));
  assert(!c.atualizar(9100,-1,true,9000));
  c.rearmar();c.solicitar(true,10000);
  assert(!c.atualizar(10000,NAN,false,0));
  c.rearmar();assert(!c.atualizar(11000,35,false,0));assert(!c.nivelValido());
  nexus::ControleAgua r;assert(r.calibrar(30,10));
  uint32_t inicio=0xFFFFF800UL;r.solicitar(true,inicio);
  assert(r.atualizar(static_cast<uint32_t>(inicio+3999),20,true,inicio));
  assert(!r.atualizar(static_cast<uint32_t>(inicio+4000),20,true,inicio));
  puts("OK: 26 verificacoes da logica de agua; nenhum acionamento fisico ensaiado.");
}
