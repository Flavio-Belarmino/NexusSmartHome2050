# Interfaces e reserva de pinos: nova montagem

Mapa preliminar, não instrução de ligação completa. A pinagem definitiva será publicada após identificação e teste dos módulos. [R06 histórica](Pinagem_Mega_R06.csv).

| Grupo | Interface prevista | Reserva ou decisão |
| --- | --- | --- |
| TFT shield paralelo de 8 bits | Dados e comandos em encaixe tipo Uno | No mapeamento padrão da biblioteca: D2–D9 e A0–A4; conferir shield físico e exemplo usado |
| Touch resistivo | Compartilha pinos com o TFT | Descobrir pares e calibrar antes de ligar outros periféricos |
| DS3231 e AHT25 | I²C | Mega: SDA 20 e SCL 21; verificar alimentação e níveis dos módulos antes de compartilhar o barramento |
| RC522 | SPI | Mega: MISO 50, MOSI 51, SCK 52; SS e RST próprios por leitor; não ligar os dois kits inicialmente |
| SD do shield | SPI com seleção própria | Desativado no primeiro ensaio; encaixe tipo Uno pode exigir adaptação ao SPI do Mega |
| Servo MG996R | Sinal do firmware R06 em D30 | Preservar como referência; alimentação externa e GND comum |
| Dois SG90 | Sinais próprios | Pinos e comportamento a definir depois de identificar curso e mecanismo |
| Botões e semáforos | Entradas/saídas digitais | Alocar após fechar ocupação do shield e sinais anteriores |
| Sensores IR de obstáculo | Saída digital e/ou analógica conforme módulo | Conferir saídas, polaridade e ajuste reais |
| Receptor IR KY-022 | Entrada digital | Confirmar biblioteca, protocolo e compatibilidade de temporizadores com Servo e demais saídas |
| Barra WS2812 | Uma linha de dados, alimentação própria | Pino livre a definir; integrar efeitos depois de validar temporização e alimentação |
| LEDs RGB avulsos | Três canais por LED/grupo | Resistores individuais; acionamento dimensionado conforme corrente |
| Fita RGB 12 V | Controlador recebido ou interface de potência compatível | Não conectar canais de potência diretamente ao Mega |
| Bomba, relé, LDR e sensores da R06 | Interfaces anteriores | Conferir tensão e estado seguro antes de reaproveitar a ligação |

A biblioteca do display faz diagnóstico e calibração usando sinais compartilhados. Por isso o teste inicial mantém os demais componentes desconectados. A distribuição antiga não deve ser misturada com a nova sem conferir cada pino.

Para cada alocação final, preencher: componente, terminal, pino Mega, tensão lógica, fonte, estado ao ligar, resultado individual e fotografia. Não atribuir ao novo firmware funções presentes apenas nas telas demonstrativas.
