# Materiais consolidados R02

NEXUS | 06/11/2026 | Base: inventário declarado e documentos publicados até esta revisão.

Esta lista reúne o estoque **declarado**, as reservas por função e os complementos previstos. Nenhum saldo foi conferido fisicamente. “Não identificado” significa que o documento não comprova a disponibilidade, e não que o grupo necessariamente precisa comprar. Quantidades propostas não são autorização nem pedido de compra. Valores e custos permanecem em aberto, sem preços inventados.

## Começar pela conferência

1. Reunir os componentes e conferir as 51 linhas abaixo, anotando modelo e quantidade real.
2. Identificar fontes, bateria/controlador, bomba, solenoide, vazão, fita, touch, relé, ESP32 e câmeras.
3. Separar o microservo para o brise e o HC-SR04 para o reservatório. Compartilhar PIR/LDR na integração; não contar o mesmo sensor duas vezes.
4. Escolher os complementos que a versão física usará. Medir percursos e mecanismos antes de fechar a compra.

## Inventário e destinação

Os nomes e as quantidades de origem foram preservados, inclusive descrições que precisam de correção após a leitura das etiquetas. Uma linha pode representar kit, peça ou lote. As quantidades não devem ser somadas como se todas fossem unidades iguais.

| ID | Descrição original | Qtd. declarada | Função/reserva | Observação |
| --- | --- | --- | --- | --- |
| I01 | ARDUINO MEGA 2560 C/ CABO | 1 | Controle local | 1 placa compartilhada por todas as funções; ensaios atuais separados |
| I02 | ESP32 DUAL CORE WIFI/BLOETOOTH | 1 | Supervisão/rede | 1 placa reservada; interface e firmware de comunicação pendentes |
| I03 | CONTROLADOR DE CARGA | 1 | Solar | Ensaio separado; identificar modelo e compatibilidade |
| I04 | COMPONENTES ELETRONICOS KG | 1 | Avulsos | Lote descrito em kg; conteúdo não discriminado, não abater complementos por suposição |
| I05 | BATERIA 12V 7A | 1 | Solar | Manter descrição original 12V 7A; confirmar química, capacidade e etiqueta |
| I06 | FONTE 12V 5A | 2 | Alimentação | 2 fontes declaradas; destinação após conferir cargas e conectores |
| I07 | FONTE 5V 3A | 2 | Alimentação | 2 fontes declaradas; destinação após conferir cargas e conectores |
| I08 | FITA DE LED PC 10M | 1 | Iluminação | 1 peça declarada como 10 m; tipo/tensão/comprimento útil a conferir |
| I09 | MODULO SENSOR TOQUE CAPACITIVO 4 CANAIS TTP32 | 1 | Comandos locais | 1 módulo; identificação TTP32/4 canais a confirmar |
| I10 | MODULO SENSOR SONAR HC-SR04 | 1 | Água A05 | 1 reservado ao nível do reservatório; não alocar ao portão |
| I11 | MODULO SENSNOR DE LUMINOSIDADE LDR 5MM 3 PINOS KY-018 | 1 | Luz A01 e brise A02 | 1 sensor compartilhado no projeto integrado; bancada em momentos separados |
| I12 | SENSOR DE UMIDADE E TEMPERATURA DHT22- AM2302 TEMPERATUARA -40ºC A +80ºC TENSÃO 3a 5V | 1 | Ambiente A04 | 1 para leituras; não existe climatização acionada neste módulo |
| I13 | SENSOR DE MOVIMENTO E PRESENÇA SR-501 | 1 | Luz A01 e intrusão | 1 PIR compartilhado; não há um sensor disponível por ambiente |
| I14 | SENSOR DE FLUXO OU VAZÃO TIPO HALL-75A 570ML/MIN | 1 | Água A05 | 1; modelo, saída e calibração pendentes |
| I15 | MINI BOMBA D'AGUA RS-385 C DE TRABALHO 0,5-0,7A TENSÃO 12V | 1 | Água A05 | 1 bomba de bancada; acionamento não implementado no sketch atual |
| I16 | LED AMARELO | 5 | Sinalização | 5 amarelos; alocação final por canal pendente |
| I17 | LED VERDE | 5 | Sinalização | 5 verdes; alocação final por canal pendente |
| I18 | LED VERMELHO | 5 | Sinalização | 5 vermelhos; alocação final por canal pendente |
| I19 | LED BRANCO | 20 | Iluminação | 20 brancos; quantidade instalada e resistores a definir |
| I20 | MICRO SERVO 9G 3,0-7,2V 180º | 1 | Brise A02 | 1 reservado ao brise; portão precisa de atuação própria |
| I21 | MINI SOLENOIDE 6V FECHADURA ELETRONICA | 1 | Acesso A03 | 1; corrente/regime e conjunto de acionamento pendentes |
| I22 | MINI PLACA SOLAR FOTOVOTAICO 12V 125mA 85X115MM 1,5W | 1 | Solar | 1 painel de 1,5 W conforme inventário; ensaio independente do FV residencial |
| I23 | MODULO RELÊ 5V 10A | 1 | Interface de carga | 1 módulo; número de canais e aplicação ainda não confirmados |
| I24 | BOTÕES | 20 | Comandos | 20; repartir entre ensaios e comandos após mapa final |
| I25 | BOTÃO DE EMERGÊNCIA | 1 | Parada | 1; contatos e comportamento físico a identificar |
| I26 | KIT LEITOR REFID RC522-13,56MHZ CARTÃO E CHAVEIRO | 1 | Acesso A03 | 1 kit; conteúdo cartão/chaveiro conforme descrição, conferir fisicamente |
| I27 | PROTOBOARD 830 PONTOS | 1 | Bancada | 1; reutilizável entre ensaios, não presumir uma por função |
| I28 | KIT JUNPER MACHO X MACHO 40 PEÇAS | 1 | Bancada | 1 kit anunciado com 40 peças; conferir saldo e qualidade |
| I29 | KIT JUMPER FÊMEA X FÊMEA 40 PEÇAS | 1 | Bancada | 1 kit anunciado com 40 peças; conferir saldo e qualidade |
| I30 | KIT JUMPER MACHO X FÊMEA 40 PEÇAS | 1 | Bancada | 1 kit anunciado com 40 peças; conferir saldo e qualidade |
| I31 | CAMÊRA VGA OV7670 | 2 | Vídeo | 2; captura/interface ainda não implementadas |
| I32 | RESISTOR 1R | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I33 | RESISTOR 10R | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I34 | RESISTOR 47R | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I35 | RESISTOR 56R | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I36 | RESISTOR 100R | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I37 | RESISTOR 220R | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I38 | RESISTOR 330R | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I39 | RESISTOR 470R | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I40 | RESISTOR 560R | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I41 | RESISTOR 1K | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I42 | RESISTOR 10K | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I43 | RESISTOR 47K | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I44 | RESISTOR 56K | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I45 | RESISTOR 100K | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I46 | RESISTOR 220K | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I47 | RESISTOR 330K | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I48 | RESISTOR 470K | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I49 | RESISTOR 560K | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I50 | RESISTOR 1M | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |
| I51 | RESISTOR 10M | 5 | Resistores | 5 por valor no inventário; selecionar por circuito, não tratar valores como intercambiáveis |

Existem 35 LEDs discretos declarados, além da fita. Isso não define 35 LEDs instalados. O estoque de resistores contém 20 valores com cinco peças de cada; os 100 resistores não são intercambiáveis. O saldo do valor escolhido depende do circuito e da quantidade que será montada. A protoboard, o Mega, PIR, LDR e botões podem ser reutilizados entre ensaios; testes separados não exigem automaticamente novas placas/sensores.

## Complementos da maquete

| ID | Função | Complemento | Quantidade de referência | Situação documental | Antes de selecionar/comprar |
| --- | --- | --- | --- | --- | --- |
| M01 | RFID | Interface de níveis e alimentação compatíveis com o RC522 | 1 conjunto | Não identificado | Identificar placa/interface e conferir guia A03 antes de selecionar |
| M02 | Mega/ESP32 | Interface de comunicação entre placas | 1 enlace | Não identificado | Definir protocolo, pinos e conversão apropriada à interface |
| M03 | Bomba | Driver, proteção e conexões da bomba | 1 canal/conjunto | Não identificado | Conferir corrente de partida/regime e carga antes da especificação |
| M04 | Solenoide | Driver, proteção e alimentação compatível com a peça de 6 V | 1 canal/conjunto | Não identificado | Fontes de 5/12 V do inventário não comprovam alimentação adequada |
| M05 | Fita LED | Acionamento e conexões da fita | A definir por trecho/canal | Não identificado | Fotografar marcações e medir trechos antes de quantificar |
| M06 | Brise | Suporte, articulação e ligação mecânica | 1 conjunto | Não discriminado | Ensaiar curso livre do mecanismo antes da fixação |
| M07 | Garagem | Atuação própria do portão | 1 conjunto | Não identificado | Medir massa, vão e curso; não usar a reserva do brise |
| M08 | Garagem | Detecção externa, interna e presença no vão | 3 funções | Não identificado | Quantidade de dispositivos depende da solução; não assumir 3 HC-SR04 |
| M09 | Garagem | Confirmação de aberto/fechado | 2 estados | Não identificado | Definir retorno próprio ou sensores; não somar automaticamente 2 sensores |
| M10 | Acesso/intrusão | Contatos de porta | 2 propostos | Não identificado | Proposta da rede R01; definir contatos, montagem e interface |
| M11 | Vazamento | Dispositivos de detecção de água | 2 propostos | Não identificado | VA01/VA02; escolher tecnologia e demonstrar evento físico |
| M12 | Fumaça | Dispositivo para demonstração de detecção | 1 proposto | Não identificado | Definir solução da maquete; não apresentar simulador como detecção real |
| M13 | Alarmes | Sinalizador e interface | 1 conjunto proposto | Não identificado | Tipo, potência, nível sonoro e acionamento a definir |
| M14 | Vídeo | Arquitetura de captura das OV7670 | 1 solução a definir | Não identificado | Conferir FIFO, pinagem e interface antes de decidir complementos |
| M15 | Água | Reservatório, recipiente de retorno e bandeja | 1 conjunto de bancada | Não discriminado | Dimensões e volumes após teste; não confundir com reservatórios prediais |
| M16 | Água | Mangueiras, conexões e fixações | A medir | Não discriminado | Diâmetro pelas peças reais; traçado acessível e estanqueidade em bancada |
| M17 | Instalação | Cabos, bornes e conectores identificados | A medir por percurso | Não discriminado | Jumpers disponíveis não comprovam toda a instalação permanente |
| M18 | Instalação | Proteções, seccionamento, distribuição e caixas DC | A especificar por ramo | Não discriminado | Conferir fontes/cargas; sem lista fechada de fusíveis por suposição |
| M19 | Luz | Resistores individuais e suportes de LEDs | 1 resistor por LED instalado | Estoque por valor na tabela | Quantificar LEDs por canal e selecionar valores segundo o guia; saldo ainda indefinido |
| M20 | Montagem | Fixadores, espaçadores e pontos de inspeção | A quantificar | Não discriminado | Testar acesso a placas, fontes e conexões antes de fechar paredes |
| M21 | Civil maquete | MDF 3 mm e peças de fechamento | Pelo plano de corte e saldo | Saldo não informado | Não repetir a compra das peças já adquiridas; conferir cortes |
| M22 | Garagem | Papelão Paraná, mecanismo e fixação | A medir | Saldo não informado | Espessura e dimensão após carrinho e vão |
| M23 | Exposição | Base, apoios e fixação de transporte | 1 conjunto proposto | Saldo não informado | Base 1200 x 900 x 18 mm é proposta; confirmar peso/transporte antes de comprar |
| M24 | Solar | Interfaces/proteções e instrumentos do ensaio | A definir | Compatibilidade não comprovada | Identificar controlador, bateria e painel antes de seleção |
| M25 | Bancada | Instrumentos e computador USB | Conjunto de apoio | Disponibilidade não informada | Confirmar empréstimo/disponibilidade antes de comprar |

## Materiais da residência representada

Esta seção documenta o projeto acadêmico da casa. **Não é lista de compras da maquete.** Quantitativos de obra, perdas, peças de catálogo, compatibilidade final e preços não foram levantados. Os critérios de cálculo e seus limites continuam no [dimensionamento R02](../../06_Calculos/Dimensionamento_R02/).

| ID | Grupo | Quantidade de referência | Origem | Limite da quantidade |
| --- | --- | --- | --- | --- |
| R01 | Pontos de luz e comandos | 11 + 11 posições | Elétrica R01 | Contar luminárias, lâmpadas e mecanismos depois de selecionar produtos |
| R02 | Tomadas de uso geral | 28 pontos | Elétrica R01 | Não somar TUE como novas TUG nem confundir ponto com número de módulos |
| R03 | Quadro | 1, previsão de pelo menos 72 módulos | Dimensionamento R02 | Capacidade física/térmica final depende dos produtos |
| R04 | Circuitos de carga | 20 circuitos | Dimensionamento R02 | Proteções individuais C1-C20; C21 é geração |
| R05 | Proteção geral / DPS / equipotencialização | Conjuntos do unifilar | Dimensionamento R02 | Modelos e acessórios pendentes; consultar unifilar |
| R06 | Condutores e eletrodutos | Por circuito; metragem final pendente | Circuitos_R02.csv | Comprimento de cálculo não é quantitativo de compra; depende de condutores/rotas/folgas |
| R07 | Cooktop / forno / micro-ondas / geladeira / depurador | 1 de cada | C8/C9/C10/C11/C16 | Potências de estudo; não são componentes a comprar para a maquete |
| R08 | Lavadora | 1 | C12 / H09 | Equipamento residencial de referência |
| R09 | Ar-condicionado | 2 | C14/C15 | Modelos/capacidades e instalação a selecionar |
| R10 | Portão e central de rede/automação | 1 conjunto de cada | C18/C17 | Não equivalem ao microservo e Mega da maquete |
| R11 | Módulos fotovoltaicos / inversor | 6 x 550 Wp / 1 de 3 kW | Solar R02 | Produtos e compatibilidade pendentes; painel de bancada é outro item |
| R12 | Reservatório potável / cisterna não potável | 1 de 1000 L nominal de cada | Hidráulica R02 | 800 L úteis de estudo em cada; reservatórios no solo |
| R13 | Pressurização AF / NP | 2 bombas AF + 2 NP | Hidráulica R02 | Principal/reserva; uma ativa por conjunto, não quatro simultâneas |
| R14 | Aquecedor central / vaso de expansão | 1 de 200 L e 3 kW / 1 de 18 L | Hidráulica R02 | Conjunto de segurança, mistura e acessórios por fabricante |
| R15 | Pia / lavatórios / bacias / chuveiros / tanque | 1 / 2 / 2 / 2 / 1 | H01-H08 | Lavadora em R08; não duplicar H09 |
| R16 | Ralos / caixas sifonadas | 2 / 2 | H10/H11 / CS1/CS2 | Contagem funcional; peças e acabamento a detalhar |
| R17 | Caixa de gordura / inspeção | 1 CG1 / 4 CI1-CI2-CI3-CIE | Esgoto R02 | DS1 é limite/conexão de estudo, não uma quinta caixa |
| R18 | Ventilação | 5 terminais DN50 | Ventilacao_R02.csv | Tubulação e conexões dependem dos percursos finais |
| R19 | Água, esgoto e redes de chuva | Redes por diâmetro; metragem final pendente | Trechos/CAD R02 | Comprimentos de perda e comprimentos equivalentes não viram compra direta |
| R20 | Calha / descidas / desvio inicial | 14,35 m / 2 DN100 / 1 recipiente de 200 L | Chuva R02 | Quantitativo geométrico de estudo; acessórios, bocais e folgas pendentes |
| R21 | Tratamento e reposição não potável | 1 conjunto de cada | Hidráulica R02 | Requisitos de desempenho no memorial; não há produto final selecionado |
| R22 | Rede: dados / AP / câmeras IP | 4 pontos / 1 AP / 2 câmeras | Rede R01 | Não são as duas OV7670; 7 enlaces propostos |
| R23 | Rede: ONT/roteador/switch e cabeamento | Conjunto a selecionar | Rede R01 | Capacidade proposta >=10 portas; comprimentos não incluem percurso final/folgas |
| R24 | Materiais civis da residência | A definir | Arquitetura R02 | Sem sistema construtivo escolhido; MDF da maquete não é especificação da residência |

## Fontes e rastreabilidade

- [Inventário original](../Inventario_Original_Eletronicos.pdf) e [transcrição JSON](../Inventario_Eletronicos.json): origem das 51 linhas, sem reclassificar estoque não identificado como zero.
- [Identificação por função](../Identificacao_e_Complementos.md) e [especificação de automações](../../04_Automacao/NEXUS_Especificacao_Automacoes_R01.txt): reservas e interfaces pendentes.
- [Complementos de rede e segurança](../../05_Seguranca/Rede_R01/Complementos_por_Escopo.csv): quantidades propostas M10-M13 e R22-R23.
- [Pontos elétricos R01](../../02_Eletrica/Residencial_R01/) e [modelo dimensionado R02](../../06_Calculos/Dimensionamento_R02/Modelo_Dimensionamento_R02.json): cenário residencial.
- [Dados desta consolidação](BOM_Consolidada_R02.json): inventário, complementos e itens residenciais, com IDs estáveis para registrar as próximas conferências.

Para atualizar: informar o ID, a quantidade física, o modelo/etiqueta e a decisão de uso. Registrar depois a quantidade instalada e o custo real com comprovante. Só calcular saldo/compra quando necessidade e disponibilidade tiverem a mesma unidade e especificação.
