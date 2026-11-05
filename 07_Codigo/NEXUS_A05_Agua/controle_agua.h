#ifndef NEXUS_CONTROLE_AGUA_H
#define NEXUS_CONTROLE_AGUA_H
#include <stdint.h>
namespace nexus {
class ControleAgua {
 public:
  bool calibrar(float vazio,float cheio){
    calibrado_=false;pedido_=permitido_=false;
    if(!(vazio>=2&&vazio<=400&&cheio>=2&&cheio<=400&&vazio-cheio>=2))return false;
    vazio_=vazio;cheio_=cheio;calibrado_=true;return true;
  }
  void solicitar(bool pedido,uint32_t agora){if(pedido && !pedido_)inicio_=agora;pedido_=pedido;if(!pedido)permitido_=false;}
  void rearmar(){falha_=false;pedido_=permitido_=false;}
  bool atualizar(uint32_t agora,float distancia,bool fluxoMonitorado,uint32_t ultimoPulso){
    nivelValido_=calibrado_ && distancia>=2 && distancia<=400 && distancia<=vazio_+3 && distancia>=cheio_-3;
    nivel_=-1;
    if(nivelValido_){nivel_=100*(vazio_-distancia)/(vazio_-cheio_);if(nivel_<0)nivel_=0;if(nivel_>100)nivel_=100;}
    if(pedido_ && (!nivelValido_ || nivel_<20))falha_=true;
    if(pedido_ && fluxoMonitorado && static_cast<uint32_t>(agora-inicio_)>=4000 && static_cast<uint32_t>(agora-ultimoPulso)>=4000)falha_=true;
    return permitido_=pedido_ && nivelValido_ && nivel_>=20 && !falha_;
  }
  bool calibrado()const{return calibrado_;} bool nivelValido()const{return nivelValido_;}
  bool falha()const{return falha_;} float nivel()const{return nivel_;}
 private:
  bool calibrado_=false,nivelValido_=false,pedido_=false,permitido_=false,falha_=false;
  float vazio_=0,cheio_=0,nivel_=-1;
  uint32_t inicio_=0;
};
}
#endif
