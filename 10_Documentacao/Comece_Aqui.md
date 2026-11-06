# Como vamos desenvolver o NEXUS

Casa Inteligente | NEXUS | ExpoTech. 06/11/2026.

O projeto será desenvolvido com entregas pequenas e verificáveis. A equipe não precisa dominar previamente todas as disciplinas para começar; precisa entender as decisões adotadas, conferir o que foi montado e registrar os resultados.

## Divisão prática do trabalho

| Parte | Preparação técnica com assistência | Participação necessária da equipe |
| --- | --- | --- |
| Plantas e instalações | Elaborar desenhos, tabelas, premissas e memórias de cálculo; compatibilizar revisões | Confirmar decisões de uso e conferir medidas que dependem da montagem |
| Automação | Escrever o código comentado, orientar conexões, testar a lógica e corrigir com base nos resultados | Carregar o programa, realizar as ligações e os ensaios orientados |
| Materiais | Cruzar inventário com os circuitos e especificar complementos | Conferir os modelos recebidos e efetuar as compras necessárias |
| Documentação | Organizar arquivos, revisar textos, registrar versões e atualizar o GitHub | Fornecer fotos, vídeos, nomes e resultados reais dos testes |

Decisões ainda abertas serão apresentadas com uma proposta e sua justificativa. Uma hipótese de estudo precisa ser identificada antes de entrar no cálculo ou no desenho. Uma dimensão conferida na montagem deve substituir a estimativa na revisão correspondente.

## Primeira entrega de programação disponível

[A01: iluminação na bancada](../07_Codigo/NEXUS_A01_Bancada/README.md). Inclui firmware inicial para Mega, ligações por função, comandos de teste, calibração de luminosidade e ficha para registrar o resultado. Pode ser preparada antes de montar a casa.

O primeiro passo físico é separar os componentes e identificar as marcações dos sensores. Em seguida, testar o LED manualmente; depois as leituras; por último o automático. Se uma etapa falhar, registrar o erro e corrigir antes de acrescentar outra função.

## O que continua avançando sem a montagem

Os [projetos prediais dimensionados R02](../06_Calculos/Dimensionamento_R02/) estão disponíveis: elétrica com cargas, fases, cabos/proteções, quadro/unifilar e geração; hidráulica com pressões, diâmetros, reservação, aquecimento, esgoto/ventilação e chuva. Os cálculos e dez grupos de testes podem ser reproduzidos sem Colab. São estudos separados dos circuitos DC e da recirculação da maquete.

A equipe pode estudar as pranchas e conferir as hipóteses antes da montagem. A aplicação real depende das verificações externas e de fabricantes listadas no memorial. O [guia de preparação do ensaio de água](../03_Hidraulica/Residencial_R01/Preparacao_Ensaio_Agua.md) permite iniciar identificação e bancada. Nenhum desses documentos depende de já haver LED colado ou sensor fixado na casa.

Os módulos de ambiente, brise, acesso, água e comandos já têm programas de bancada preparados no [kit R02](Guia_Bancada_Modulos.md). A garagem tem uma simulação funcional de sequência, com geometria e atuação físicas ainda dependentes do carrinho e do mecanismo. Ensaiar os programas separadamente antes da revisão integrada.

## Critério para integrar na casa

Integrar um módulo depois de conferir alimentação, ligação e resposta no ensaio de bancada. Fixar de forma que fios, conexões e componentes possam ser inspecionados. Completar a ficha de teste e associá-la à versão do programa. Um programa escrito e compilado ainda precisa desse teste físico.

## Próximo ensaio sem montagem

A [rede e segurança R01](../05_Seguranca/Rede_R01/) já traz plantas, topologia, complementos e simulador de alarmes. Extrair o [ZIP](../05_Seguranca/Rede_R01/NEXUS_Simulador_Alarmes_R01.zip), abrir o HTML e seguir os três testes na tela: intrusão armada, fumaça/água independentemente de armar e perda de amostras. A lógica foi testada por software; a equipe deve conferir a interface e registrar o resultado. O registro exportado continua identificado como simulação.

A identificação dos componentes e os testes de bancada permanecem necessários antes da integração física. Sensores adicionais não recebem pinos por tentativa e o estudo residencial de rede não obriga comprar ONT/switch/câmeras IP para a maquete.
