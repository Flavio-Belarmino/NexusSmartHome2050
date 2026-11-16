# Automação

**Referência da montagem atual: [Automação integrada R06](Automacao_Integrada_R06.md).**

- [Firmware integrado e instruções](../07_Codigo/NEXUS_TFT_Integrado_R06/README.md).
- [Pinagem atual em CSV](Pinagem_Mega_R06.csv) e [guia de ligação em PDF](../10_Documentacao/Guias/NEXUS_Guia_Pratico_Pinagens_R06.pdf).
- [Registro de ensaios e pendências](../09_Simulacoes/Validacao/Registro_Ensaios_R06.csv).

A montagem atual usa Mega, TFT/touch, MG996R, RC522, LDR, DHT22, sensor resistivo de água, boia/sensor de nível, relé, bomba, LEDs e botões. O buzzer permanece associado a uma falha de reinício do Mega em investigação. Ensaios de bancada foram relatados; a verificação final após remontagem continua pendente.

## Documentos de referência anteriores

A [especificação R01](NEXUS_Especificacao_Automacoes_R01.pdf), a [versão em texto](NEXUS_Especificacao_Automacoes_R01.txt) e as [interfaces do kit antigo](Interfaces_e_Integracao.md) foram preservadas. Descrevem funções propostas e módulos independentes, com pinagens diferentes da integração atual.

A detecção de passagem, obstáculo e posição pertence à especificação/simulação da garagem, não ao firmware físico R06. O microservo do brise e o HC-SR04 do inventário não foram reclassificados como dispositivos instalados. ESP32, solenoide, fumaça, câmeras, vazão e experimento solar não são acionados pela R06.
