# Casa Inteligente | NEXUS | ExpoTech

Projeto acadêmico da categoria **BLUEPRINT**, Engineering 2026.2, UniFECAF. Integra o estudo da residência, instalações, uso de água e energia, automação e segurança.

**Entrega atual:** [índice e pendências R06](10_Documentacao/Entrega_R06.md) · [caderno técnico R04](10_Documentacao/Caderno_Tecnico/NEXUS_Caderno_Tecnico_R04.pdf) · [firmware integrado R06](07_Codigo/NEXUS_TFT_Integrado_R06/) · [pinagem em PDF](10_Documentacao/Guias/NEXUS_Guia_Pratico_Pinagens_R06.pdf).

## Estado atual - 16/11/2026

A publicação reúne o projeto residencial R02 e a configuração de automação que está sendo transferida da bancada para a maquete. O Arduino Mega possui firmware integrado para TFT/touch, portão com MG996R e RFID, iluminação por LDR, DHT22 com alarme, detecção de água e bomba comandada por sensor de nível.

A equipe relatou testes físicos bem-sucedidos em bancada das funções individuais e de uma integração anterior. A revisão R06 foi compilada e passou nos testes de lógica em computador. **A remontagem na casa e o ensaio final de todas as funções ainda precisam de registro.** O reaparecimento da abertura NEXUS durante o alarme foi identificado como reinício do Mega; a causa permanece em investigação. A presença de fonte externa não foi tratada como prova de estabilidade.

O firmware R06 controla o portão entre 0° e 90°: botão/TFT mantêm a posição; RFID autorizado abre e fecha após 3 s, ou apenas fecha se já estiver aberto/abrindo. Não há detecção de obstáculo nem confirmação física de posição nesta montagem. A sequência mais completa do simulador de garagem permanece como estudo separado.

ESP32/Wi-Fi, brise, CFTV, detecção de fumaça, vazão e microgeração continuam como propostas, inventário ou estudos, conforme seus documentos; não são funções físicas implementadas pelo R06. A garagem física ainda precisa ser compatibilizada com as plantas R02.

## Consultar os arquivos

**Montagem atual:** [regras R06](04_Automacao/Automacao_Integrada_R06.md), [pinagem CSV](04_Automacao/Pinagem_Mega_R06.csv) e [componentes da montagem](08_BOM/Componentes_Montagem_R06.csv). Os módulos antigos abaixo possuem pinagens próprias e não devem ser usados como guia de ligação da R06.

| Conteúdo | Arquivo ou pasta | Situação |
| --- | --- | --- |
| Plantas, implantação, cobertura, fachadas e cortes | [PDF de 23 pranchas](01_Arquitetura/R02/PDF/NEXUS_Casa_Inteligente_ExpoTech_Plantas.pdf) | Anteprojeto R02 |
| Desenhos editáveis | [26 arquivos DXF](01_Arquitetura/R02/DXF/) | Arquitetura, maquete e sistemas propostos |
| Dimensões dos ambientes, aberturas e adjacências | [Dados CSV e JSON](01_Arquitetura/R02/DADOS/) | Cotas de trabalho em milímetros |
| Elétrica residencial | [Dimensionamento R02](06_Calculos/Dimensionamento_R02/) | 20 circuitos de carga, geração C21, cabos/proteções e unifilar; cenário acadêmico calculado |
| Elétrica DC da maquete | [Elétrica](02_Eletrica/) | Proposta R02, a compatibilizar com os módulos reais |
| Hidráulica residencial | [Dimensionamento R02](06_Calculos/Dimensionamento_R02/) | Água, pressões, reservação, aquecimento, esgoto/ventilação e chuva calculados nas hipóteses declaradas |
| Especificação funcional de referência R01 | [Especificação R01 em PDF](04_Automacao/NEXUS_Especificacao_Automacoes_R01.pdf) · [texto editável](04_Automacao/NEXUS_Especificacao_Automacoes_R01.txt) | Estudo original; montagem atual descrita na R06 |
| Segurança e rede | [Plantas e topologia R01](05_Seguranca/Rede_R01/) | Posições/interfaces propostas e simulador de alarmes; hardware/rede ainda pendentes |
| Quantitativos e premissas | [Cálculos](06_Calculos/) | Memórias prediais R02 disponíveis; custos, base de exposição e ensaios a complementar |
| Gerador dos desenhos | [Código Python](07_Codigo/Gerador_Documentacao/) | Código de documentação; não controla a maquete |
| Primeiro módulo de controle (histórico) | [A01: iluminação na bancada](07_Codigo/NEXUS_A01_Bancada/) | Firmware inicial e testes de lógica; ensaio físico pendente |
| Demais módulos de bancada (histórico) | [Índice de código](07_Codigo/README.md) | Brise, RFID, ambiente, água, botões e entradas; compilados, com ensaio físico pendente |
| Alarmes computacionais | [Simulador offline](05_Seguranca/Rede_R01/NEXUS_Simulador_Alarmes_R01.zip) | 18 cenários de lógica testados, sem sensores reais; interface visual pendente |
| Garagem computacional | [Simulador funcional](09_Simulacoes/Garagem/README.md) | Sequência testada por software, sem mecanismo real |
| Telemetria local | [Supervisor USB](07_Codigo/Supervisor_USB/README.md) | Programa e API testados; porta USB real ainda não ensaiada |
| Experimento solar | [Cálculo e balanço de potências](06_Calculos/Solar/README.md) | Estimativas explícitas, sem ensaio de carga/autonomia |
| Materiais e componentes | [BOM consolidada R02](08_BOM/Consolidacao_R02/) | 51 linhas de inventário, reservas, complementos e itens residenciais; conferência física/custos pendentes |
| Ensaios | [Registro atual R06](09_Simulacoes/Validacao/Registro_Ensaios_R06.csv) e [validação de software](07_Codigo/NEXUS_TFT_Integrado_R06/Validacao_Software_R06.md) | Relatos de bancada separados dos testes executados e das evidências ainda a anexar |
| Memorial e requisitos | [Memorial R03](10_Documentacao/Memorial_Consolidado_R03.md) e [compatibilização R06](10_Documentacao/Compatibilizacao_R06.md) | Escopo residencial e montagem atual separados |
| Vídeo pitch | [Orientação atual e roteiro R06](11_Pitch/) | Até 5 min conforme orientação recente do professor; todos devem aparecer; vídeo a gravar |

## Dimensões e leitura das plantas

O piso da maquete tem **717,5 × 308 mm**. O modelo R02 relaciona a representação arquitetônica à maquete pelo fator 20. As unidades e escalas estão indicadas nas vistas e no [LEIA-ME da R02](01_Arquitetura/R02/LEIA-ME.txt). As dimensões internas são estimativas de trabalho do anteprojeto, sujeitas à conferência durante a montagem.

A base de exposição de **1.200 × 900 × 18 mm** é uma proposta, a compatibilizar com peso, apoios, transporte e garagem. A espessura gráfica das paredes ampliadas não define o sistema construtivo da residência.

## Instalações e implementação

As pranchas E01 a E10 representam a **elétrica DC da maquete**. A [revisão predial dimensionada R02](06_Calculos/Dimensionamento_R02/) acrescenta dois cadernos de seis pranchas, quatro DXFs, tabelas e cálculos reproduzíveis. A elétrica define cargas, fases, seções, proteções, unifilar e entrada fotovoltaica para o cenário trifásico adotado. A hidráulica calcula vazões, perdas, pressões, reservação, aquecimento, cotas de esgoto, ventilação e chuva. Os pontos elétricos R01 permanecem como referência; as novas rotas hidráulicas substituem as divergentes da R01, principalmente a pia/CG1.

Os cálculos fecham nas hipóteses declaradas. Fornecimento e conexões reais, fichas dos equipamentos, coordenação das proteções, curvas das bombas, chuva/local e condições do lote ainda exigem conferência antes de execução. A [rede e segurança R01](05_Seguranca/Rede_R01/) propõe posições, topologia e interfaces, com alarmes virtuais testados por software; cobertura, dispositivos, rede e atuação física continuam pendentes.

O controle local da montagem está descrito no [guia do firmware integrado](07_Codigo/NEXUS_TFT_Integrado_R06/README.md). O ESP32 não participa do firmware R06. A elétrica DC da maquete usa fontes externas de 5 V separadas para servo e TFT, GND comum e alimentação própria da bomba. Modelo do buzzer e tensão nominal do módulo relé ainda precisam de identificação antes de fechar a remontagem.

## O que falta para fechar esta entrega

1. Concluir a remontagem e resolver os reinícios associados ao alarme/acionamentos.
2. Registrar o teste final do conjunto, fotos, resultados e limites; conferir a garagem na planta e a lista realmente instalada.
3. Gravar o vídeo com todos os integrantes, publicar link acessível e atualizar o cadastro do portal.
4. Conferir o texto de stack e o link público de documentação no [índice de entrega](10_Documentacao/Entrega_R06.md).

O código, os desenhos e os cálculos não substituem os resultados físicos. Não se declaram comunicação ESP32, desempenho energético ou detecção de obstáculos que não tenham sido implementados e demonstrados.

## Referências e versão de entrega

Os documentos oficiais consultados estão em [Regulamento](10_Documentacao/Regulamento/). As referências técnicas já utilizadas para as interfaces constam do LEIA-ME R02. Outras fontes técnicas devem ser acrescentadas às decisões que fundamentarem. Os arquivos de trabalho não constituem projeto liberado para execução de uma residência real.

Identificar o commit apresentado na defesa. O aviso recente do portal prorroga cadastro/alterações de grupos até 12h de 16/11; não é tratado aqui como alteração automática das demais datas do regulamento. O item 9 do regulamento proíbe alterar projeto, código ou documentação após a avaliação individual; a equipe precisa confirmar com o professor responsável como tratar as melhorias mencionadas no item 4.

## Guias anteriores de desenvolvimento

O [guia do grupo R02](10_Documentacao/Guia_Grupo_R02.md) registra a etapa anterior de preparação dos materiais e ensaios. Para a remontagem atual, usar a pinagem R06. Antes de comprar ou fechar a maquete, consultar a [BOM consolidada](08_BOM/Consolidacao_R02/) e as [24 interfaces de compatibilização](10_Documentacao/Compatibilizacao_R02.md).
