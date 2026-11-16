# Memorial consolidado R03

NEXUS | Casa Inteligente | BLUEPRINT | 16/11/2026

Esta revisão conserva o cenário residencial dimensionado R02 e atualiza a implementação demonstrativa para o firmware integrado R06. A [R02](Memorial_Consolidado_R02.md) permanece como histórico. Resultados de simulação, relatos de bancada e ensaios finais não são tratados como equivalentes.

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

O Arduino Mega executa o firmware integrado R06. TFT ILI9341 com touch apresenta cinco páginas e comandos; navegação também por botões 25/26. O MG996R do portão recebe comandos de 0°/90° pelo botão, TFT e RC522. Dois identificadores de demonstração são autorizados. O fechamento após RFID ocorre depois de 3 s de espera; não há sensores de obstáculo, passagem ou confirmação de posição no hardware programado. O simulador com sequência completa é um estudo separado.

Iluminação por LDR usa limiares com histerese e permite modo manual. DHT22 informa temperatura/umidade; a partir de 30 °C o LED/buzzer sinaliza, com cancelamento físico/touch e rearme após <=29,5 °C. TESTAR na tela aciona por 3 s sem aquecimento. Falha de leitura produz aviso global. A sonda C113 é utilizada como detector demonstrativo de presença de água; sensor NPN de nível comanda a bomba por relé, com desligamento em HIGH e prioridade sobre pedido manual.

A instalação usa fontes externas de 5 V separadas para servo e TFT, GND comum e positivos separados; bomba alimentada em 12 V pelo relé. Tensão nominal do módulo relé e modelo/interface do buzzer ainda precisam de identificação. O reaparecimento da abertura NEXUS durante o alarme é reinício do Mega relatado e não foi diagnosticado como resolvido.

ESP32/Wi-Fi, brise, solenoide, câmeras, fumaça, vazão e microgeração não integram a R06. A topologia residencial e as simulações permanecem como estudos. O relógio é de software, sem RTC; volume do reservatório e posição do portão na tela são animações sem sensores contínuos de realimentação.

## Materiais e montagem

A [BOM consolidada R02](../08_BOM/Consolidacao_R02/) preserva o inventário de origem. A [relação da montagem R06](../08_BOM/Componentes_Montagem_R06.csv) acrescenta o TFT, MG996R, sonda C113, sensor de nível e interfaces atuais, sem inventar custo ou quantidade final instalada. Kits, lotes e funções de software não são somados como peças.

A remontagem mantém componentes acessíveis à inspeção, conexões identificadas e separação entre circuitos demonstrativos e instalações residenciais do estudo. Medidas da garagem/base e configuração final devem ser registradas. A [pinagem atual](Guias/NEXUS_Guia_Pratico_Pinagens_R06.pdf) prevalece sobre a pinagem de módulos antigos.

## Sustentabilidade e critérios ESG

| Escolha | Justificativa de projeto | Indicador disponível | O que falta comprovar |
| --- | --- | --- | --- |
| Uso de chuva nas descargas | Substituição de parte da demanda potável no cenário | Demanda NP de estudo de 120 L/dia | Balanço climático anual, qualidade e operação; não equivale a economia anual obtida |
| Geração fotovoltaica | Propor fonte renovável na residência | Potência instalada proposta de 3,30 kWp | Produção, sombras, consumo de referência, conexão e economia |
| Iluminação por luminosidade | Ajustar funcionamento à luz ambiente | LDR e comando manual no firmware R06 | Ensaios finais e consumo comparativo; presença não integra a R06 e não há percentual de economia |
| Brise | Propor controle da incidência de luz | Comando e posições de ensaio previstos | Orientação, clima, geometria, desempenho térmico e luz natural |
| Componentes acessíveis/reutilizáveis | Facilitar manutenção e reduzir descarte de peças | Inventário e proposta de montagem desmontável | Fotografias, massa reaproveitada e registro de manutenção/desmontagem |
| Documentação e acesso ao conhecimento | Tornar decisões, código e limites verificáveis | Arquivos públicos, guias e testes de software | Participação/treinamento de todos e evidências de execução |

Esses itens são critérios de acompanhamento. Não constituem certificação ambiental, autossuficiência ou resultado social/ambiental medido. A reserva nominal de água e a potência fotovoltaica, isoladamente, não demonstram sustentabilidade do conjunto.

## Validação e pendências

Há registros anteriores de cálculos e simuladores e, nesta revisão, compilação para Mega e testes reproduzíveis da lógica R06. A equipe relatou funcionamento em bancada de servo/botão, servo/RFID, TFT/touch, LDR, DHT, água e bomba/nível. Esses relatos foram registrados sem inventar datas, medições ou evidências anexadas. A remontagem completa e o ensaio final precisam de comprovação, e o reinício ao acionar alarme/atuadores permanece aberto.

Consultar o [registro de ensaios](../09_Simulacoes/Validacao/Registro_Ensaios_R06.csv) e a [compatibilização atual](Compatibilizacao_R06.md). Para encerrar: identificar interfaces pendentes, repetir ensaio do conjunto, registrar fotos/vídeo, conferir garagem/material civil e cadastrar os links de entrega. Não se atribui a simulação desempenho mecânico ou economia física.

## Documentos de referência

- [Arquitetura R02](../01_Arquitetura/R02/) e [pontos elétricos R01](../02_Eletrica/Residencial_R01/).
- [Dimensionamento R02, referências e limites](../06_Calculos/Dimensionamento_R02/README.md) e [verificação dos cálculos](../06_Calculos/Dimensionamento_R02/Verificacao_R02.md).
- [Automação atual R06](../04_Automacao/Automacao_Integrada_R06.md), [fonte R06](../07_Codigo/NEXUS_TFT_Integrado_R06/), [caderno R04](Caderno_Tecnico/NEXUS_Caderno_Tecnico_R04.pdf) e referência [Automações R01](../04_Automacao/NEXUS_Especificacao_Automacoes_R01.txt), [rede/segurança R01](../05_Seguranca/Rede_R01/) e [índice do código](../07_Codigo/README.md).
- [Guia dos ensaios](Guia_Bancada_Modulos.md), [controle de entregas](Controle_de_Entregas.md) e [documentos oficiais recebidos](Regulamento/).

Os documentos técnicos de origem mantêm suas premissas, referências e limites. A R03 consolida o estado do trabalho; não libera execução de residência real nem declara revisão profissional integral.
