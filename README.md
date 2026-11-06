# Casa Inteligente | NEXUS | ExpoTech

Projeto acadêmico da categoria **BLUEPRINT**, Engineering 2026.2, UniFECAF. Integra o estudo da residência, instalações, uso de água e energia, automação e segurança.

**Para começar:** [guia de desenvolvimento acompanhado](10_Documentacao/Comece_Aqui.md) e [primeiro ensaio de iluminação na bancada](07_Codigo/NEXUS_A01_Bancada/README.md). O ensaio inclui programa inicial, ligações e ficha de resultados; a montagem da casa não é pré-requisito.

**Kit de módulos R02:** [guia e ordem dos ensaios](10_Documentacao/Guia_Bancada_Modulos.md) · [pacote ZIP](07_Codigo/NEXUS_Kit_Modulos_R02.zip) · [simulador da garagem](09_Simulacoes/Garagem/README.md) · [supervisor USB](07_Codigo/Supervisor_USB/README.md). Cada sketch de bancada é independente; carregar outro programa no Mega substitui o anterior.

## Estado atual

Esta publicação reúne o **anteprojeto R02** e a **especificação funcional de automação R01**. A maquete ainda está em preparação para montagem. O funcionamento das automações, a supervisão por ESP32 e os resultados dos ensaios ainda precisam ser implementados e demonstrados. A presença de desenhos, pinagem ou regras de controle não comprova funcionamento físico.

A extensão com **garagem em papelão Paraná** faz parte do escopo atual. O controle prevê aproximação, passagem, confirmação de posição e interrupção/reabertura por obstáculo. As dimensões do carrinho, do vão e do mecanismo ainda serão compatibilizadas. Essa ampliação **ainda não está representada nas plantas R02**. O atuador da garagem será próprio; o servo do brise e o HC-SR04 do reservatório continuam reservados às suas funções.

## Consultar os arquivos

| Conteúdo | Arquivo ou pasta | Situação |
| --- | --- | --- |
| Plantas, implantação, cobertura, fachadas e cortes | [PDF de 23 pranchas](01_Arquitetura/R02/PDF/NEXUS_Casa_Inteligente_ExpoTech_Plantas.pdf) | Anteprojeto R02 |
| Desenhos editáveis | [26 arquivos DXF](01_Arquitetura/R02/DXF/) | Arquitetura, maquete e sistemas propostos |
| Dimensões dos ambientes, aberturas e adjacências | [Dados CSV e JSON](01_Arquitetura/R02/DADOS/) | Cotas de trabalho em milímetros |
| Elétrica residencial | [Pontos, cargas e circuitos R01](02_Eletrica/Residencial_R01/) | Estudo inicial publicado; dimensionamento final pendente |
| Elétrica DC da maquete | [Elétrica](02_Eletrica/) | Proposta R02, a compatibilizar com os módulos reais |
| Hidráulica residencial | [Pontos e redes R01](03_Hidraulica/Residencial_R01/) | Distribuição inicial de água/esgoto/ventilação e chuva; dimensionamento pendente |
| Regras de automação, incluindo garagem | [Especificação R01 em PDF](04_Automacao/NEXUS_Especificacao_Automacoes_R01.pdf) · [texto editável](04_Automacao/NEXUS_Especificacao_Automacoes_R01.txt) | Especificação funcional, sem firmware validado |
| Segurança e rede | [Segurança](05_Seguranca/) | Proposta a detalhar e validar |
| Quantitativos e premissas | [Cálculos](06_Calculos/) | Dados preliminares, sem memória predial concluída |
| Gerador dos desenhos | [Código Python](07_Codigo/Gerador_Documentacao/) | Código de documentação; não controla a maquete |
| Primeiro módulo de controle | [A01: iluminação na bancada](07_Codigo/NEXUS_A01_Bancada/) | Firmware inicial e testes de lógica; ensaio físico pendente |
| Demais módulos de bancada | [Índice de código](07_Codigo/README.md) | Brise, RFID, ambiente, água, botões e entradas; compilados, com ensaio físico pendente |
| Garagem computacional | [Simulador funcional](09_Simulacoes/Garagem/README.md) | Sequência testada por software, sem mecanismo real |
| Telemetria local | [Supervisor USB](07_Codigo/Supervisor_USB/README.md) | Programa e API testados; porta USB real ainda não ensaiada |
| Experimento solar | [Cálculo e balanço de potências](06_Calculos/Solar/README.md) | Estimativas explícitas, sem ensaio de carga/autonomia |
| Componentes disponíveis | [Inventário](08_BOM/) | Inventário recebido; complementos e custo final pendentes |
| Ensaios | [Plano de validação](09_Simulacoes/Validacao/) | Fichas de ensaio físico; resultados de software registrados separadamente |
| Memorial e requisitos | [Documentação](10_Documentacao/) | Memorial base e controle de pendências |
| Vídeo de até 3 minutos | [Roteiro de pitch](11_Pitch/) | Rascunho para preencher com demonstrações reais |

## Dimensões e leitura das plantas

O piso da maquete tem **717,5 × 308 mm**. O modelo R02 relaciona a representação arquitetônica à maquete pelo fator 20. As unidades e escalas estão indicadas nas vistas e no [LEIA-ME da R02](01_Arquitetura/R02/LEIA-ME.txt). As dimensões internas são estimativas de trabalho do anteprojeto, sujeitas à conferência durante a montagem.

A base de exposição de **1.200 × 900 × 18 mm** é uma proposta, a compatibilizar com peso, apoios, transporte e garagem. A espessura gráfica das paredes ampliadas não define o sistema construtivo da residência.

## Instalações e implementação

As pranchas E01 a E10 representam a **elétrica DC da maquete**. A [elétrica residencial R01](02_Eletrica/Residencial_R01/) já apresenta iluminação, comandos, tomadas, previsão de cargas e sete circuitos propostos. Ainda faltam equipamentos e fornecimento definidos, dimensionamento de condutores/proteções, quadro/unifilar, entrada de energia e integração renovável. A [hidráulica residencial R01](03_Hidraulica/Residencial_R01/) apresenta distribuição de água fria/quente/não potável, rotas de esgoto/ventilação e aproveitamento de chuva como estudo inicial. Ainda faltam seus dimensionamentos e a consolidação da rede e da segurança exigidos pelo BLUEPRINT.

O controle proposto utiliza Arduino Mega para os comandos locais e reserva ESP32 para comunicação/supervisão. Os módulos e interfaces ainda precisam de identificação e compatibilização. O experimento solar deve ser validado separadamente antes de qualquer integração de alimentação. Os parâmetros de controle dependem dos ensaios, sem presumir autonomia, economia ou precisão não medidas.

## Como evoluir esta entrega

1. Compatibilizar o projeto com as medidas conferidas, a garagem e os componentes identificados.
2. Completar os projetos prediais e as respectivas memórias de cálculo.
3. Incorporar firmware comentado, bibliotecas, versão das placas e instruções de reprodução.
4. Executar os testes, guardar evidências e registrar falhas e limites.
5. Gravar o pitch e conferir os links públicos antes da entrega.

O [controle de entregas](10_Documentacao/Controle_de_Entregas.md) distingue os arquivos existentes das partes em desenvolvimento. Há testes de lógica, compilação e uma simulação funcional da sequência da garagem, identificados no [registro de validação](07_Codigo/Testes_Modulos/Validacao_Modulos_R02.md). Os ensaios físicos e a integração completa continuam pendentes.

## Referências e versão de entrega

Os documentos oficiais consultados estão em [Regulamento](10_Documentacao/Regulamento/). As referências técnicas já utilizadas para as interfaces constam do LEIA-ME R02. Outras fontes técnicas devem ser acrescentadas às decisões que fundamentarem. Os arquivos de trabalho não constituem projeto liberado para execução de uma residência real.

Identificar o commit apresentado na defesa. O item 9 do regulamento proíbe alterar projeto, código ou documentação após a avaliação individual; a equipe precisa confirmar com o professor responsável como tratar as melhorias mencionadas no item 4.
