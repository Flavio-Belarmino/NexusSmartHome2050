# Memorial consolidado R02

NEXUS | Casa Inteligente | BLUEPRINT | 06/11/2026

Esta revisão atualiza o memorial base R01 com as instalações calculadas e os módulos publicados. É um projeto acadêmico em desenvolvimento. Distingue o cenário residencial, a representação física e a evidência já disponível. Substitui o memorial base como referência do estado atual; a R01 permanece como histórico.

## Programa e arquitetura

O cenário aprovado considera quatro moradores, dois quartos e dois banheiros, com sala, cozinha, serviço, circulação e apoio. A documentação arquitetônica R02 usa fator 20 entre maquete e residência: piso de 717,5 x 308 mm na maquete e envelope de paredes de 697,5 x 288 mm, correspondente a 13,95 x 5,76 m no modelo residencial. A espessura de MDF de 3 mm não define vedação, estrutura ou material da residência.

A garagem integra o escopo funcional, com extensão em papelão Paraná, mas ainda não está incorporada à geometria das plantas. Carrinho, vão, massa e mecanismo permanecem pendentes. A base de exposição de 1200 x 900 x 18 mm é uma proposta que depende de peso, apoio e transporte. Sistema construtivo da casa, orientação/local do estudo, conforto térmico e detalhamento civil ainda precisam de definição. Não se declara atendimento integral de acessibilidade pela leitura das cotas.

## Instalações elétricas da residência

A distribuição R01 contém 11 pontos de iluminação, 11 posições de comando e 28 TUG. A revisão de dimensionamento R02 acrescenta os circuitos C1-C20 de carga e o circuito C21 de geração. O cenário adota alimentação trifásica 127/220 V, 60 Hz, TT e soma integral das cargas, sem desconto pela geração. A potência aparente de estudo é de aproximadamente 29,624 kVA. Cabos, proteções, fases, quadro, queda de tensão e unifilar estão calculados no caderno de seis pranchas.

Os equipamentos previstos incluem cooktop, forno, micro-ondas, geladeira, depurador, lavadora, dois aparelhos de ar-condicionado, aquecedor central, portão, pressurização e central de rede. Potências e fatores de potência são hipóteses documentadas, não medições de aparelhos comprados. O cálculo não prova fornecimento aprovado, aterramento ensaiado ou coordenação de um produto escolhido.

A geração residencial proposta tem seis módulos de 550 Wp, totalizando 3,30 kWp, e inversor on-grid de 3 kW. As hipóteses de tensão, corrente e compatibilidade estão no dimensionamento. Não foram calculadas produção anual, economia financeira ou autonomia. Esse sistema não é o painel de 1,5 W do inventário da maquete.

Referência técnica e condições de aplicação: [caderno e memória R02](../06_Calculos/Dimensionamento_R02/), incluindo as fontes já consultadas e as verificações externas pendentes. Esta consolidação não altera os critérios nem representa uma nova auditoria normativa.

## Água, aquecimento, esgoto e chuva

O modelo adota 150 L por pessoa/dia, totalizando 600 L/dia. A parcela de descargas é de 120 L/dia. Foram previstos um reservatório potável e uma cisterna não potável de 1000 L nominais cada, com 800 L úteis de estudo, instalados no solo. Os conjuntos AF e NP têm duas bombas cada, alternadas, com uma ativa por conjunto.

O aquecimento central é de acumulação, 200 L e 3 kW. AF, AQ, esgoto, ventilação e chuva têm redes, vazões, diâmetros, perdas, pressões e cotas de estudo documentados. O esgoto da pia foi revisto para chegar à caixa de gordura externa pela cozinha, evitando a passagem anterior sob a sala. A revisão não resolve por si a interface estrutural e a posição real da rede pública.

A chuva utiliza área de cobertura de 85,756 m². Intensidade de 180 mm/h e desvio inicial de 2 mm são hipóteses do cenário, não série climática local. O uso NP foi reservado às descargas; tratamento, identificação e separação das redes estão previstos. Não há resultado laboratorial ou eficiência anual demonstrada. Curvas de bombas, aquecedor, tratamento, bocais e condições do lote permanecem como seleção/detalhamento externo no [dimensionamento R02](../06_Calculos/Dimensionamento_R02/).

## Automação, comunicação e segurança

O Mega é o controlador local proposto; o ESP32 está reservado para comunicação/supervisão. Foram publicados módulos independentes para iluminação, brise, RFID, ambiente, água, botões e entradas touch. Os sketches possuem guias e registros de compilação/testes de software. Carregar outro sketch na única placa Mega substitui o anterior. A integração em firmware único e a comunicação física entre placas permanecem pendentes.

O primeiro teste de RFID sinaliza autorização em LED; não demonstra acionamento da solenoide. O módulo de água verifica leitura e permissão lógica; não aciona a bomba. O microservo permanece reservado ao brise e o HC-SR04 ao reservatório. O portão exige atuação própria, detecções de aproximação/passagem/vão e confirmação de posição, conforme a especificação.

A rede R01 contém topologia e posições propostas. Os simuladores de garagem e alarmes exercitam regras lógicas. O supervisor USB permite demonstração identificada e possui ensaios de software, mas isso não comprova uma instalação física ou comunicação Mega/ESP32. Duas OV7670 constam do inventário; captura de vídeo não foi implementada. Contatos de porta, fumaça, vazamento e sinalização ainda dependem de identificação/seleção e ensaio.

## Materiais e montagem

A [BOM consolidada R02](../08_BOM/Consolidacao_R02/) conserva 51 linhas de inventário e acrescenta destinação, reservas, complementos e materiais residenciais por referência. Estoque físico, quantidades instaladas e preços continuam pendentes. Kits e lotes não são somados como peças individuais. O documento orienta a conferência antes de qualquer compra.

Propõe-se montagem com componentes identificados e pontos acessíveis de inspeção. Esse critério permite testar e substituir peças sem destruir a representação. Reservatórios/mangueiras de bancada não equivalem às redes dimensionadas da residência. A instalação DC da maquete continua sendo um projeto separado da instalação residencial.

## Sustentabilidade e critérios ESG

| Escolha | Justificativa de projeto | Indicador disponível | O que falta comprovar |
| --- | --- | --- | --- |
| Uso de chuva nas descargas | Substituição de parte da demanda potável no cenário | Demanda NP de estudo de 120 L/dia | Balanço climático anual, qualidade e operação; não equivale a economia anual obtida |
| Geração fotovoltaica | Propor fonte renovável na residência | Potência instalada proposta de 3,30 kWp | Produção, sombras, consumo de referência, conexão e economia |
| Iluminação por presença/luz | Ajustar funcionamento ao uso e à luminosidade | Regra implementada em módulo de bancada | Ensaios físicos e consumo comparativo; sem percentual de economia |
| Brise | Propor controle da incidência de luz | Comando e posições de ensaio previstos | Orientação, clima, geometria, desempenho térmico e luz natural |
| Componentes acessíveis/reutilizáveis | Facilitar manutenção e reduzir descarte de peças | Inventário e proposta de montagem desmontável | Fotografias, massa reaproveitada e registro de manutenção/desmontagem |
| Documentação e acesso ao conhecimento | Tornar decisões, código e limites verificáveis | Arquivos públicos, guias e testes de software | Participação/treinamento de todos e evidências de execução |

Esses itens são critérios de acompanhamento. Não constituem certificação ambiental, autossuficiência ou resultado social/ambiental medido. A reserva nominal de água e a potência fotovoltaica, isoladamente, não demonstram sustentabilidade do conjunto.

## Validação e pendências

Há registros de compilação dos módulos, testes de lógica dos simuladores e dez grupos de verificações internas do dimensionamento. Não existem nesta revisão evidências de ensaio físico concluído ou demonstração integrada de todas as funções. Para cada ensaio, registrar configuração, versão do código, estímulo, resposta esperada, resultado observado e evidência, incluindo falhas.

Antes de fechar a maquete: conferir inventário, resolver interfaces, testar cada módulo em bancada, incorporar a garagem, verificar acesso e registrar a integração. A [matriz de compatibilização](Compatibilizacao_R02.md) apresenta os itens concretos de conferência. O [guia do grupo](Guia_Grupo_R02.md) organiza o estudo e a primeira reunião.

## Documentos de referência

- [Arquitetura R02](../01_Arquitetura/R02/) e [pontos elétricos R01](../02_Eletrica/Residencial_R01/).
- [Dimensionamento R02, referências e limites](../06_Calculos/Dimensionamento_R02/README.md) e [verificação dos cálculos](../06_Calculos/Dimensionamento_R02/Verificacao_R02.md).
- [Automações R01](../04_Automacao/NEXUS_Especificacao_Automacoes_R01.txt), [rede/segurança R01](../05_Seguranca/Rede_R01/) e [índice do código](../07_Codigo/README.md).
- [Guia dos ensaios](Guia_Bancada_Modulos.md), [controle de entregas](Controle_de_Entregas.md) e [documentos oficiais recebidos](Regulamento/).

Os documentos técnicos de origem mantêm suas premissas, referências e limites. A R02 consolida o estado do trabalho; não libera execução de residência real nem declara revisão profissional integral.
