# Código-fonte

Disponíveis:

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

O gerador Python não controla o Arduino/ESP32. Os sketches publicados são módulos separados de bancada, não um firmware único. Na única placa Mega do inventário, carregar outro sketch substitui o anterior. A validação física e a integração continuam pendentes. Não juntar os arquivos `.ino` numa mesma pasta.

As regras que orientarão essa implementação estão na [especificação funcional](../04_Automacao/NEXUS_Especificacao_Automacoes_R01.txt). Nenhum teste de automação física está declarado como concluído.
