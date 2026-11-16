# Automação integrada R06

Configuração documentada em 16/11/2026. Controlador: Arduino Mega 2560. [Fonte integral](../07_Codigo/NEXUS_TFT_Integrado_R06/NEXUS_TFT_Integrado_R06.ino).

## Interfaces e regras efetivamente programadas

| Função | Entrada / comando | Resposta R06 |
| --- | --- | --- |
| TFT ILI9341 e touch resistivo | Toque e navegação física 25/26 | 5 páginas: início, iluminação, garagem, água, clima; troca automática a cada 3 s; interação manual pausa e AUTO retoma |
| Portão | Botão 32 ou TFT | Alterna/comanda 0° fechado e 90° aberto; mantém posição até outro comando |
| RFID RC522 | Dois UIDs de demonstração cadastrados | Se fechado/fechando, abre e fecha após 3 s de espera; se aberto/abrindo, manda somente fechar; outro UID é negado |
| Sinalização do portão | Estado comandado do servo 30 | LED 33 durante movimento e 250 ms de acomodação |
| Iluminação | LDR A9 | Escuro em leitura <=400; claro >=500; mantém estado entre os limiares; saída 34 em LOW liga; comando manual/AUTO pelo TFT |
| Temperatura e umidade | DHT22 no 22, leitura a cada 2,5 s fora do giro do servo | Mostra leituras; termômetro muda de azul a vermelho; não aciona ar-condicionado |
| Alarme de temperatura | Temperatura >=30 °C | LED 23 e buzzer 44 intermitentes, 250 ms ligados/250 ms desligados, tom de 2000 Hz |
| Cancelamento | Botão físico 24 ou SILENCIAR no TFT | Silencia teste/alarme; alarme térmico cancelado só rearma após temperatura <=29,5 °C |
| Teste manual do alarme | TESTAR na página clima | Buzzer e LED por 3 s sem alterar a temperatura; PARAR ou SILENCIAR interrompem; não cancela um alarme térmico real por expirar |
| Falha do DHT | Leitura de temperatura inválida | Aviso global por 3 s, uma vez por episódio; sugere verificar sensor/conexões; conserva o estado anterior do alarme |
| Água / vazamento | AO do sensor C113 no A8 | Leitura <=800 liga LED 28; >=900 desliga; leitura analógica a cada 100 ms |
| Bomba e nível | Sensor NPN no 43, relé no 42 | HIGH desliga imediatamente; LOW estável por 200 ms permite ligar; relé em LOW liga; modo manual não ignora a boia |
| Relógio por software | Data/hora da compilação e ajuste Serial | H AAAA-MM-DD HH:MM:SS, 9600 baud e Nova linha; reinício volta à hora da compilação; não há RTC |

O sensor de água é uma sonda resistiva de umidade do solo utilizada como detector demonstrativo de presença de água. Não foi caracterizada como detector comercial de inundação. A saída de nível é interpretada conforme a lógica relatada/testada pela equipe; conferir os dois estados físicos após remontar.

## Movimento físico e representação na tela

O servo recebe um comando por tempo decorrido: 1° por 10 ms, cerca de 0,9 s para 90°, sem realimentação. Essa é a duração nominal do comando, não uma medição mecânica sob carga. A animação do portão dura aproximadamente 3,6 s e é independente do motor. A animação de água é ilustrativa: a boia fornece dois estados, não uma porcentagem de volume. Lua branca representa escuro e sol amarelo representa claridade; o modo manual da lâmpada não altera a condição medida pelo LDR.

## Alimentação e montagem

Servo e TFT têm fontes externas distintas de 5 V. Negativos DC e GND do Mega compartilham referência; positivos dessas fontes permanecem separados. Bomba em fonte de 12 V através dos contatos do relé; pino 42 é somente comando. VCC do módulo relé deve seguir a tensão nominal da placa, ainda a conferir. RC522 em 3,3 V, com redução de nível em SS/SCK/MOSI/RST; MISO direto. Manter resistores dos LEDs e pull-up do DHT conforme montagem.

## Limites conhecidos

- Abertura NEXUS reaparece ao soar o alarme: reinício do Mega relatado, causa não diagnosticada; não foi declarado resolvido pela troca do som.
- Confirmar se o buzzer tem dois terminais ou é módulo de três pinos e dimensionar sua interface antes de concluir a instalação.
- Sem confirmação de posição, obstáculo ou passagem no portão físico; a R06 não representa um comando seguro de portão residencial real.
- Não há integração Mega/ESP32, Wi-Fi, CFTV, brise, vazão, fumaça ou microgeração neste firmware.
- Medidas finais da garagem e da base e evidências da montagem precisam ser anexadas.

## Validação

[Testes de software](../07_Codigo/NEXUS_TFT_Integrado_R06/Validacao_Software_R06.md) verificam regras com entradas simuladas. [Registro físico](../09_Simulacoes/Validacao/Registro_Ensaios_R06.csv) distingue relatos de bancada das evidências e do teste final que ainda faltam. Não foi informado horário/duração de testes físicos nem preenchida medição elétrica por suposição.
