# Casa Inteligente | NEXUS | ExpoTech

Projeto acadêmico da categoria **BLUEPRINT**, Engineering 2026.2, UniFECAF. Integra o estudo da residência, instalações, uso de água e energia, automação e segurança.

## Estado atual

Esta publicação reúne o **anteprojeto R02** e a **especificação funcional de automação R01**. A maquete ainda está em preparação para montagem. O funcionamento das automações, a supervisão por ESP32 e os resultados dos ensaios ainda precisam ser implementados e demonstrados. A presença de desenhos, pinagem ou regras de controle não comprova funcionamento físico.

A extensão com **garagem em papelão Paraná** faz parte do escopo atual. O controle prevê aproximação, passagem, confirmação de posição e interrupção/reabertura por obstáculo. As dimensões do carrinho, do vão e do mecanismo ainda serão compatibilizadas. Essa ampliação **ainda não está representada nas plantas R02**. O atuador da garagem será próprio; o servo do brise e o HC-SR04 do reservatório continuam reservados às suas funções.

## Consultar os arquivos

| Conteúdo | Arquivo ou pasta | Situação |
| --- | --- | --- |
| Plantas, implantação, cobertura, fachadas e cortes | [PDF de 23 pranchas](01_Arquitetura/R02/PDF/NEXUS_Casa_Inteligente_ExpoTech_Plantas.pdf) | Anteprojeto R02 |
| Desenhos editáveis | [26 arquivos DXF](01_Arquitetura/R02/DXF/) | Arquitetura, maquete e sistemas propostos |
| Dimensões dos ambientes, aberturas e adjacências | [Dados CSV e JSON](01_Arquitetura/R02/DADOS/) | Cotas de trabalho em milímetros |
| Elétrica DC da maquete | [Elétrica](02_Eletrica/) | Proposta R02, a compatibilizar com os módulos reais |
| Hidráulica residencial | [Hidráulica](03_Hidraulica/) | Detalhamento e dimensionamento pendentes |
| Regras de automação, incluindo garagem | [Especificação R01 em PDF](04_Automacao/NEXUS_Especificacao_Automacoes_R01.pdf) · [texto editável](04_Automacao/NEXUS_Especificacao_Automacoes_R01.txt) | Especificação funcional, sem firmware validado |
| Segurança e rede | [Segurança](05_Seguranca/) | Proposta a detalhar e validar |
| Quantitativos e premissas | [Cálculos](06_Calculos/) | Dados preliminares, sem memória predial concluída |
| Gerador dos desenhos | [Código Python](07_Codigo/Gerador_Documentacao/) | Código de documentação; não controla a maquete |
| Componentes disponíveis | [Inventário](08_BOM/) | Inventário recebido; complementos e custo final pendentes |
| Ensaios | [Plano de validação](09_Simulacoes/Validacao/) | Resultados ainda não registrados |
| Memorial e requisitos | [Documentação](10_Documentacao/) | Memorial base e controle de pendências |
| Vídeo de até 3 minutos | [Roteiro de pitch](11_Pitch/) | Rascunho para preencher com demonstrações reais |

## Dimensões e leitura das plantas

O piso da maquete tem **717,5 × 308 mm**. O modelo R02 relaciona a representação arquitetônica à maquete pelo fator 20. As unidades e escalas estão indicadas nas vistas e no [LEIA-ME da R02](01_Arquitetura/R02/LEIA-ME.txt). As dimensões internas são estimativas de trabalho do anteprojeto, sujeitas à conferência durante a montagem.

A base de exposição de **1.200 × 900 × 18 mm** é uma proposta, a compatibilizar com peso, apoios, transporte e garagem. A espessura gráfica das paredes ampliadas não define o sistema construtivo da residência.

## Instalações e implementação

As pranchas E01 a E10 representam a **elétrica DC da maquete**. O projeto elétrico residencial, com previsão de cargas, tomadas, circuitos, quadro, entrada de energia e dimensionamento de condutores/proteções, ainda precisa ser desenvolvido. Também faltam o detalhamento hidráulico predial e a consolidação da rede e da segurança exigidos pelo BLUEPRINT.

O controle proposto utiliza Arduino Mega para os comandos locais e reserva ESP32 para comunicação/supervisão. Os módulos e interfaces ainda precisam de identificação e compatibilização. O experimento solar deve ser validado separadamente antes de qualquer integração de alimentação. Os parâmetros de controle dependem dos ensaios, sem presumir autonomia, economia ou precisão não medidas.

## Como evoluir esta entrega

1. Compatibilizar o projeto com as medidas conferidas, a garagem e os componentes identificados.
2. Completar os projetos prediais e as respectivas memórias de cálculo.
3. Incorporar firmware comentado, bibliotecas, versão das placas e instruções de reprodução.
4. Executar os testes, guardar evidências e registrar falhas e limites.
5. Gravar o pitch e conferir os links públicos antes da entrega.

O [controle de entregas](10_Documentacao/Controle_de_Entregas.md) distingue os arquivos existentes das partes em desenvolvimento. Não há nesta publicação resultados experimentais ou simulações funcionais concluídas.

## Referências e versão de entrega

Os documentos oficiais consultados estão em [Regulamento](10_Documentacao/Regulamento/). As referências técnicas já utilizadas para as interfaces constam do LEIA-ME R02. Outras fontes técnicas devem ser acrescentadas às decisões que fundamentarem. Os arquivos de trabalho não constituem projeto liberado para execução de uma residência real.

Identificar o commit apresentado na defesa. O item 9 do regulamento proíbe alterar projeto, código ou documentação após a avaliação individual; a equipe precisa confirmar com o professor responsável como tratar as melhorias mencionadas no item 4.
