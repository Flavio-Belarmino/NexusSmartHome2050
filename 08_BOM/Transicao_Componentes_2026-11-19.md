# Componentes: substituições e novas integrações

Revisão de 19/11/2026. Fonte da compra: planilha Smart_Home_2050_3a_Lista_Componentes.xlsx fornecida pela equipe. [Inventário técnico completo](Compra_3_Componentes_2026-11-19.csv).

| Componente | Quantidade nesta compra | Uso previsto | Situação da integração |
| --- | --- | --- | --- |
| TFT shield 3,5" com touch, resolução anunciada 480 × 320 | Compra separada, recebido | Substituir o display anterior e ampliar a interface | Ensaio isolado preparado; controlador e toque a confirmar |
| Protoboard BB-4TD-01, 3260 pontos | 1 | Ampliar o espaço da montagem | Conferir continuidade e divisão dos barramentos |
| Jumpers de 40 cm | 2 pacotes de 40 vias por tipo | Ligações MM, MF e FF; 80 fios de cada tipo | Usar comprimentos necessários e evitar emendas |
| Jumpers de 10 cm | 1 pacote de 40 vias por tipo | Ligações curtas MM, MF e FF | 40 fios de cada tipo |
| Fonte 5 V / 3 A, plugue P4 | 1 | Candidata à alimentação externa de circuitos de 5 V | Medir tensão, polaridade e comportamento sob carga |
| Fonte 6 V / 2 A, plugue P4 | 1 | Possível ramo de atuadores compatíveis | Não equivale a uma fonte de 5 V; uso depende das especificações reais |
| Adaptador P4 fêmea para borne | 1 | Entrada de alimentação na distribuição | Conferir polaridade |
| Fio 20 AWG, aproximadamente 0,50 mm² | 5 m vermelho + 5 m preto | Distribuição de baixa tensão | Definir rotas e conexões conforme carga e comprimento |
| Resistores 220 Ω, 330 Ω, 470 Ω, 1 kΩ, 3,3 kΩ e 10 kΩ | 20 de cada | LEDs e interfaces conforme cada circuito | 120 resistores; não há 2,2 kΩ registrado nesta compra |
| SG90 | 2 | Portas ou mecanismos leves | Conferir versão posicional ou rotação contínua antes de definir comandos |
| Receptor IR VS1838B / KY-022 | 1 | Comandos por controle remoto compatível | Confirmar controle disponível e protocolo |
| RTC DS3231 | 1 | Horário local | Testar leitura, ajuste e retenção com bateria compatível |
| Sensor IR de obstáculo LM393 | 2 | Demonstração de presença/obstáculo | Testar alcance e polaridade; não constitui proteção de segurança validada |
| AHT25 I²C | 1 | Candidato a substituir o DHT da montagem anterior | Requer driver próprio e adaptação da leitura; manter o sensor anterior como alternativa |
| Semáforo RYG de 8 mm | 2 | Sinalização de estados | Conferir pinagem e resistores incorporados |
| LEDs de alto brilho branco, azul, amarelo e vermelho | 10 de cada cor | Iluminação e sinalização | Dimensionar resistor por LED e acionamento conforme quantidade |
| LED roxo de alto brilho | 5 | Efeito visual | A compra registra alto brilho, não roxo leitoso |
| LED RGB difuso, cátodo comum | 5 | Cor e indicação de estados | Um resistor por canal; diferente do módulo KY-016 |
| Barra WS2812, oito LEDs | 1 | Efeitos endereçáveis | Teste isolado de alimentação e dados antes de integrar |
| Fita RGB 5050, 12 V, IP65, 5 m | 1 | Iluminação decorativa | Confirmar acessórios, pinagem e consumo reais; não equivale à WS2812 |
| Potenciômetros lineares WH148 | 10 valores, 1 de cada | Ajustes e demonstrações analógicas | 1k, 2k, 5k, 10k, 20k, 50k, 100k, 220k, 500k e 1M; knobs não confirmados |
| Kits RC522, cartão e chaveiro 13,56 MHz | 2 | Controle de acesso | Conferir os dois kits e níveis lógicos; usar cartões compatíveis |
| Chaveiro RFID separado, 125 kHz | 1 | Reserva para leitor compatível | A frequência registrada é diferente da dos RC522; separar dos seus cartões |
| Botões R13-507 sem trava | 6 | Comandos locais | 2 verdes, 2 vermelhos e 2 pretos; usar como entrada de baixa tensão |
| Case acrílica MAC01 para Mega | 1 | Organização e proteção | Conferir acesso aos conectores e encaixe do shield |
| Alicate de corte rente | 1 | Montagem | Ferramenta |

## Materiais anteriores e diferenças da solicitação

Mega, MG996R, sensores e circuito de água da R06, fontes anteriores e STEP POWER apresentada em foto não fazem parte desta compra. Devem ser conferidos separadamente, sem contar novamente como novos itens.

Não aparecem nesta compra: LEDs verdes avulsos, resistor de 2,2 kΩ, módulo KY-016 e fonte USB de 5 V / 2 A. Há um adaptador P4, em vez dos três solicitados. Essas diferenças não impedem começar o teste isolado do display nem devem gerar uma exigência automática de compra.

A resolução e o ILI9486 são dados do anúncio do TFT; os LVC245A visíveis no verso são circuitos de interface e não identificam o controlador do painel.

## Regras para substituir

AHT25 não usa a leitura DHT do firmware antigo. A barra WS2812 precisa de protocolo endereçável; a fita RGB de 12 V utiliza outra interface. Um SG90 de rotação contínua controla velocidade/sentido, não uma posição angular determinada. O slot SD do shield fica fora do primeiro teste, preservando a simplicidade e evitando conflitos de SPI antes da compatibilização com RFID.
