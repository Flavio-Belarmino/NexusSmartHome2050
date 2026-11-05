#ifndef NEXUS_CONTROLE_LUZ_H
#define NEXUS_CONTROLE_LUZ_H

#include <stdint.h>

namespace nexus {
enum class Modo : uint8_t { Desligado, Ligado, Automatico };

struct ConfigLuz {
  uint32_t estabilizacaoMs;
  uint32_t permanenciaMs;
  int margemAdc;
  int separacaoMinimaAdc;
};

// Logica independente de Arduino, para permitir testes deterministas em C++.
// Os tempos e limites sao parametros de bancada, nao resultados de medicao.
class ControleLuz {
 public:
  explicit ControleLuz(ConfigLuz config, uint32_t inicio)
      : config_(config), inicio_(inicio) {}

  bool calibrar(int claro, int escuro) {
    calibrado_ = false;
    escuro_ = false;
    houveMovimento_ = false;
    acesa_ = false;
    if (claro < 0 || claro > 1023 || escuro < 0 || escuro > 1023) return false;
    const int diferenca = escuro > claro ? escuro - claro : claro - escuro;
    if (config_.margemAdc <= 0 ||
        diferenca < config_.separacaoMinimaAdc ||
        diferenca <= 2 * config_.margemAdc) return false;
    centro_ = (claro + escuro) / 2;
    escuroAumentaAdc_ = escuro > claro;
    calibrado_ = true;
    return true;
  }

  void modo(Modo novo) {
    modo_ = novo;
    // Exige uma nova deteccao ao voltar ao automatico.
    houveMovimento_ = false;
    acesa_ = novo == Modo::Ligado;
  }

  bool atualizar(uint32_t agora, int luminosidade, bool movimento) {
    if (modo_ == Modo::Ligado) return acesa_ = true;
    if (modo_ == Modo::Desligado) return acesa_ = false;
    if (!calibrado_ || !pronto(agora) || luminosidade < 0 || luminosidade > 1023) {
      houveMovimento_ = false;
      return acesa_ = false;
    }
    // Histerese: duas fronteiras evitam comutacao perto do ponto central.
    if (escuroAumentaAdc_) {
      if (luminosidade >= centro_ + config_.margemAdc) escuro_ = true;
      else if (luminosidade <= centro_ - config_.margemAdc) escuro_ = false;
    } else {
      if (luminosidade <= centro_ - config_.margemAdc) escuro_ = true;
      else if (luminosidade >= centro_ + config_.margemAdc) escuro_ = false;
    }
    // Enquanto a saida do PIR permanece alta, o tempo e renovado.
    if (movimento) {
      houveMovimento_ = true;
      ultimoMovimento_ = agora;
    }
    const bool recente = houveMovimento_ &&
        static_cast<uint32_t>(agora - ultimoMovimento_) < config_.permanenciaMs;
    return acesa_ = escuro_ && recente;
  }

  bool pronto(uint32_t agora) const {
    return static_cast<uint32_t>(agora - inicio_) >= config_.estabilizacaoMs;
  }
  bool calibrado() const { return calibrado_; }
  bool escuro() const { return escuro_; }
  bool acesa() const { return acesa_; }
  int centro() const { return centro_; }
  Modo modo() const { return modo_; }

 private:
  ConfigLuz config_;
  uint32_t inicio_;
  uint32_t ultimoMovimento_ = 0;
  int centro_ = 512;
  bool escuroAumentaAdc_ = false;
  bool calibrado_ = false;
  bool escuro_ = false;
  bool houveMovimento_ = false;
  bool acesa_ = false;
  Modo modo_ = Modo::Desligado;
};
}  // namespace nexus
#endif
