# Validação em computador do A01 R01

Casa Inteligente | NEXUS | ExpoTech. 05/11/2026.

## Testes da decisão de controle

Executado `teste_logica.cpp` com g++ em C++11, com `-Wall -Wextra -Werror -pedantic`. Resultado: processo finalizado com código zero e **28 verificações aprovadas**.

Cobertura: bloqueio sem calibração; rejeição de faixa insuficiente ou inválida; espera de estabilização; movimento no claro e no escuro; histerese; desligamento na fronteira de tempo; troca manual/automático; polaridade invertida do LDR; renovação por PIR alto; recalibração inválida; transbordamento do contador de 32 bits.

## Compilação do firmware

Ferramentas efetivamente usadas:

- Arduino CLI **1.5.2-rc.1**, commit fef6e48df.
- Plataforma **arduino:avr 1.8.8**.
- Compilador **avr-gcc 7.3.0-atmel3.6.1-arduino7**.
- Alvo **arduino:avr:mega:cpu=atmega2560**.

Comando reproduzível em ambiente com a plataforma instalada:

```sh
arduino-cli compile --fqbn arduino:avr:mega:cpu=atmega2560 07_Codigo/NEXUS_A01_Bancada
```

Resultado: processo finalizado com código zero. Programa: **5.004 bytes**, de 253.952 disponíveis. Variáveis globais: **246 bytes**, de 8.192 disponíveis; restam 7.946 bytes para uso local conforme o relatório do compilador. Esses números pertencem a esta compilação; podem variar com versões das ferramentas.

## Limite da evidência

Não houve conexão com o Mega físico, upload para a placa, calibração real do LDR ou ensaio do PIR. O código está preparado para o primeiro teste de bancada, ainda sem validação física. Não houve teste dos demais sistemas da casa nesta etapa.
