# Código-fonte

## Firmware da montagem atual

[**NEXUS TFT integrado R06**](NEXUS_TFT_Integrado_R06/README.md): Mega 2560, TFT/touch, servo do portão, RFID, LDR, DHT22/alarme, sensor de água e bomba/nível. Inclui código comentado, pinagem, dependências, teste de alarme na tela, relógio e testes de lógica em computador. A instabilidade com reinício ao tocar o buzzer ainda está em investigação.

**Usar a pinagem R06 para esta montagem.** Não juntar os sketches de etapas diferentes na mesma pasta. A R06 é um único sketch e substitui o programa anterior ao ser carregada no Mega.

## Módulos anteriores e estudos preservados


- [Guia e ordem dos ensaios](../10_Documentacao/Guia_Bancada_Modulos.md) e [kit completo em ZIP](NEXUS_Kit_Modulos_R02.zip).

- [A01: iluminação na bancada](NEXUS_A01_Bancada/README.md), primeiro firmware de ensaio para Arduino Mega. Inclui comandos manuais, leitura de PIR/LDR, calibração e modo automático para um LED.
- [Testes da lógica A01](Testes_A01/README.md), executáveis em computador, sem simular a física dos sensores.
- [A02 brise](NEXUS_A02_Brise/README.md), servo livre e LDR.
- [A03 RFID](NEXUS_A03_RFID/README.md), cadastro temporário e autorização no LED; solenoide sem acionamento.
- [A04 ambiente](NEXUS_A04_Ambiente/README.md), leituras e falhas de DHT22.
- [A05 água](NEXUS_A05_Agua/README.md), nível e permissão lógica; bomba sem acionamento.
- [A08 botões/LEDs](NEXUS_A08_Botoes/README.md), canais e parada lógica.
- [A09 entradas](NEXUS_A09_Entradas/README.md), diagnóstico dos quatro canais reservados ao touch.
- [Supervisor USB](Supervisor_USB/README.md), painel local de leitura e registro CSV.
- [Validação dos novos módulos](Testes_Modulos/Validacao_Modulos_R02.md), com compilação, memória e escopo dos testes.
- [Gerador Python de documentação](Gerador_Documentacao/NEXUS_Gerador_Documentacao.py), que produz desenhos e tabelas.


O gerador Python não controla o Arduino. Os sketches A01-A09 e o kit R02 são ensaios separados anteriores à integração e possuem pinagens próprias. Registros de compilação/simulação antigos continuam identificados por revisão. O supervisor USB e o ESP32 não foram incorporados automaticamente ao firmware R06.
