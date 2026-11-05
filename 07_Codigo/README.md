# Código-fonte

Disponíveis:

- [A01: iluminação na bancada](NEXUS_A01_Bancada/README.md), primeiro firmware de ensaio para Arduino Mega. Inclui comandos manuais, leitura de PIR/LDR, calibração e modo automático para um LED.
- [Testes da lógica A01](Testes_A01/README.md), executáveis em computador, sem simular a física dos sensores.
- [Gerador Python de documentação](Gerador_Documentacao/NEXUS_Gerador_Documentacao.py), que produz desenhos e tabelas.

O gerador Python não controla o Arduino/ESP32. O A01 é um módulo inicial de bancada e ainda não reúne as demais funções da casa. Sua validação física, os outros módulos e a integração continuam pendentes.

As regras que orientarão essa implementação estão na [especificação funcional](../04_Automacao/NEXUS_Especificacao_Automacoes_R01.txt). Nenhum teste de automação física está declarado como concluído.
