# Compatibilização da montagem R06

Referência em 16/11/2026. A [matriz R02](Compatibilizacao_R02.md) permanece como histórico do projeto completo.

| Interface | Decisão atual | Pendência |
| --- | --- | --- |
| TFT e pinos compartilhados | A0-A4 e 2-9 reservados à tela/touch | Usar pinagem R06; não repetir pinos de módulos antigos |
| Analógicos | LDR A9, água A8 | Conferir após remontagem com cada sensor |
| Portão | MG996R no 30, botão 32, LED 33 | Medidas, articulação/carga, transporte e evidência; sem obstáculo/fim de curso |
| Iluminação | Saída 34 ativa em LOW | Preservar ligação/driver e conferir LEDs/corrente do conjunto |
| Temperatura | DHT22 no 22, LED 23, buzzer 44, silenciar 24 | Identificar buzzer e investigar reinício; não é alarme certificado de incêndio |
| Bomba | Relé 42 ativo em LOW; sensor 43 HIGH desliga | Identificar tensão nominal do módulo, conferir os dois estados físicos e estabilidade |
| Fontes | Servo e TFT em fontes externas distintas de 5V; GND comum | Verificar alimentação em carga e conexões; ainda não há medição documentada |
| RFID | RC522 em 3,3V; divisores nas quatro saídas do Mega | Conferir divisores e conexões após remontagem |
| Água visual | Enchimento e onda ilustrativos | Boia fornece dois estados; não declarar volume percentual medido |
| Garagem/civil | Ampliação funcional existente no escopo | Cotas finais ainda não incorporadas às plantas |
| Projeto x implementação | ESP32, brise, CFTV, fumaça, vazão e solar fora do firmware R06 | Apresentar como estudo/proposta até existir implementação e evidência |
| Versão documental | Fonte R06 e caderno R04 | Confirmar que o vídeo demonstra a mesma versão; preservar arquivos usados na avaliação |
