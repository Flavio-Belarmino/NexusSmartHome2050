# Elétrica e hidráulica dimensionadas R02

**Casa Inteligente | NEXUS | ExpoTech. 06/11/2026.** Dimensionamento esquemático acadêmico do programa aprovado: quatro moradores, cozinha elétrica, dois aparelhos de ar-condicionado, aquecimento central, automação e garagem.

Esta revisão acrescenta cálculos, seções/diâmetros, proteções, quadro/unifilar, geração, pressões, reservação, aquecimento e altimetria. Mantém a arquitetura R02 e usa as distribuições R01 como base. **Os resultados fecham internamente para as hipóteses declaradas; não representam medições de campo ou liberação para executar/energizar uma residência.** Não é a instalação DC da maquete.

## Documentos principais

| Arquivo | Conteúdo |
| --- | --- |
| [Elétrica dimensionada, 6 pranchas](NEXUS_Eletrica_Dimensionada_R02.pdf) | Cargas/fases/demanda, unifilar, distribuição, entrada fotovoltaica, condutores/proteções e memória |
| [Hidráulica dimensionada, 6 pranchas](NEXUS_Hidraulica_Dimensionada_R02.pdf) | Reservação/aquecimento, distribuição, vazões/perdas/pressões, esgoto/ventilação, cotas e chuva |
| [Modelo de cálculo](Modelo_Dimensionamento_R02.json) | Hipóteses e todos os resultados numéricos |
| [Circuitos de carga](Circuitos_R02.csv) e [geração C21](Circuito_Geracao_C21.csv) | Circuitos C1-C20; C21 é fonte, sem somar à demanda de consumo |
| [Trechos hidráulicos](Hidraulica_Trechos_R02.csv) e [pressões](Hidraulica_Pressoes_R02.csv) | Cada vazão, diâmetro interno de cálculo, comprimento, velocidade, perda e pressão de chegada |
| [Aparelhos](Aparelhos_Hidraulicos_R02.csv) | Vazões escolhidas, alturas de conexão, esgoto/UHC |
| [Cotas de esgoto](Esgoto_Cotas_R02.csv) e [ventilação](Ventilacao_R02.csv) | DN, declividades, comprimentos, cotas e terminais |
| [Unifilar DXF](E02_Unifilar_Dimensionado.dxf) e [fotovoltaica DXF](E02_Cobertura_Fotovoltaica.dxf) | Representação editável em mm |
| [Água em CAD 3D](H02_Agua_Dimensionada_3D.dxf) e [esgoto/ventilação em CAD 3D](H02_Esgoto_Dimensionado_3D.dxf) | Trajetos com alturas/cotas em mm; sem detalhar peças de catálogo |
| [Cálculos](Calcular.py), [geração das pranchas](Gerar_Entregas.py) e [testes](Testar_Dimensionamento.py) | Código reproduzível; sem dependência do Colab |
| [Verificação](Verificacao_R02.md) | Conferências realizadas e seus limites |

Os pontos de iluminação, tomadas, interruptores e suas coordenadas continuam nas [pranchas e dados elétricos R01](../../02_Eletrica/Residencial_R01/). Essa base faz parte do conjunto por referência, e a R02 define agora circuitos/condutores/proteções. As plantas gerais da [arquitetura R02](../../01_Arquitetura/R02/) permanecem válidas. Para água/esgoto, a R02 desta pasta substitui as rotas/cotas da hidráulica R01 que divergirem, principalmente a pia e CG1.

## Elétrica: decisões e resultado

- Cenário trifásico 127/220 V, 60 Hz, TT. Não há fornecimento aprovado ou ponto de conexão real identificado.
- Previsão total de cargas **29.624,336 VA** a 100% de simultaneidade, sem abater geração solar. Fases aproximadamente **76,74 / 75,81 / 75,72 A**, com cálculo fasorial e FPs declarados.
- Entrada/geral 100 A; alimentador de ida 5 m, 3F+N de 50 mm² e PE de 25 mm². Barramento mínimo 125 A por considerar entrada e ramo de geração. Quadro inicial de 72 módulos, condicionado às dimensões/dissipação dos produtos.
- Circuitos C1-C20 dimensionados; C21 de geração separado. Cada circuito com proteção residual própria e eletroduto independente. N não é compartilhado após RCBO; PE contínuo.
- Método B1, cobre/PVC 70 °C, ambiente 30 °C, sem agrupamento e sem isolamento térmico. O modelo fasorial usa FP de deslocamento e pressupõe terceira harmônica de até 15% da fundamental por fase; o limite resultante de corrente de neutro consta do JSON, mantendo a seção integral. A margem 0,80 no alimentador é adicional, não confirmação do espectro harmônico. Se as condições mudarem, recalcular.
- C1/C2 com 1,5 mm²; demais circuitos pelo menos 2,5 mm². C6, tomadas de serviço, **4 mm² por queda de tensão**. Cooktop C8 com 6 mm². Maior queda total do modelo: **3,7023%**, incluindo o alimentador.
- Dimensionamento por `Ib = S/U`, `Ib <= In <= Iz`; queda conservadora `2ρLI/S`, com ρ = 0,0225 Ω.mm²/m. Para iluminação/TUG, a potência equivalente com FP 1 é previsão de carga, não medição de watts/consumo dos aparelhos.
- Potências, FPs e comprimentos são parâmetros de projeto, não fichas de equipamentos comprados. Cada modelo escolhido depois deve caber nesses parâmetros ou exigir revisão. As duas bombas de cada conjunto são principal/reserva, intertravadas, com uma ativa; a reserva não foi somada como operação simultânea. Os circuitos alimentam o conjunto, que precisa das proteções individuais de motor.
- Icc máxima hipotética de 6,35 kA; capacidade de interrupção exigida de 10 kA. Para Icc mínima foram usadas impedâncias de fonte de 0,1 Ω fase/neutro e 0,2 Ω fase/fase, além dos cabos. Os resultados superam 10 In para os disjuntores de curva C no modelo.
- O limite térmico de cada seção é `(115 S)²`, registrado no CSV como requisito para energia passante do dispositivo. **A ficha I²t do fabricante, as partidas/inversores, o tempo de desligamento TT, Icc/loop reais e ensaios DR ainda precisam ser conferidos antes de execução.** Não há ensaio de curto ou aterramento.
- TT com BEP/equipotencialização; RA objetivo de até 20 Ω, não medida. DPS tipo II 3+1 próprio para TT, com respaldo/coordenação conforme fabricante; avaliação de SPDA/tipo I depende do local. Os parâmetros constam do memorial.

Nos banhos, foram adotados boxes de 800 × 800 mm para conferir a distribuição. T09/T24 ficam além de 600 mm da projeção desses boxes. O dimensionamento não autoriza linhas ou aparelhos nos volumes proibidos; verificar instalação, grau de proteção e equipotencialização conforme a geometria final.

### Fotovoltaica de estudo

Seis módulos de 550 Wp = 3,30 kWp; inversor on-grid de 3,00 kW, 220 V; dois MPPT independentes, três módulos em série por entrada. Parâmetros são requisitos de compatibilidade do cenário, não indicação de um produto já selecionado.

Voc de string corrigido a 10 °C: 156,75 V. Vmp a 70 °C com coeficiente hipotético de -0,35%/°C: 106,16 V. Exigir faixa MPPT que inclua 90-450 V, limite CC de pelo menos 600 V, corrente de entrada de pelo menos 15 A e Isc admissível de pelo menos 18 A por MPPT. Os módulos devem admitir a proteção gPV 20 A do esquema. Não paralelizar as strings.

CC: 6 mm², 15 m de ida, ampacidade mínima corrigida de 25 A; seccionamento e DPS por entrada. CA C21: 4 mm², 20 m, proteção 20 A e DR tipo B bidirecional conforme o inversor. Quedas de estudo: CC 1,169%; CA 1,395%. A área de módulos é 15,87 m². A instalação depende de estrutura, sombras, ventilação, temperatura, SPDA, certificação/anti-ilhamento e aceite da distribuidora. Não foi calculada energia anual ou autonomia; o sistema não possui bateria e não garante operação na falta de rede.

## Hidráulica: decisões e resultado

Consumo de estudo de 150 L/pessoa.dia, quatro pessoas: 600 L/dia. Descargas: cinco usos por pessoa/dia e seis litros por descarga, total 120 L/dia NP; rotina potável de 480 L/dia. A reserva potável verifica 600 L/dia, incluindo reposição à rede NP em falta de chuva.

- Reservatório potável de 1.000 L nominal, 800 L úteis: 1,33 dia para a demanda de backup. Cisterna NP de 1.000 L nominal, 800 L úteis, para alvo de seis dias sem entrada (720 L). Isso não comprova desempenho anual de aproveitamento de chuva.
- Reservatórios no solo, com acesso/limpeza e apoio próprio; não se coloca uma tonelada sobre a cobertura por equivalência de escala.
- AF: conjunto de duas bombas alternadas, uma ativa, **Q >= 1,45 L/s e H >= 28 mca**, potência elétrica de estudo de 1,1 kW por bomba. A vazão inclui 1,15 L/s dos usos e 0,30 L/s de reposição NP. NP: duas bombas alternadas, uma ativa, Q >= 0,30 L/s e H >= 18 mca, estudo de 370 W. Curvas, NPSH, rendimento e controle reais são condições de seleção.
- Pressões de controle: AF 250 kPa, NP 150 kPa. AF em PVC soldável DE 40/32/25/20; AQ em CPVC DE 28 e ramais DE 22; NP em PVC DE 25/20. Os diâmetros internos mínimos usados nas contas estão no CSV. Escolher classes de pressão/temperatura compatíveis.
- Vazões nominais adotadas sem redução de simultaneidade: AF+AQ de 1,15 L/s. Perdas por Darcy-Weisbach/Swamee-Jain, com `Leq = 1,5 L` como provisão para conexões. São usadas as extensões integrais dos trechos de distribuição com a vazão inicial, uma aproximação conservadora para as perdas. Não é o método de pesos da antiga NBR 5626.
- AQ reserva 50 kPa para aquecedor/grupo e 20 kPa para mistura. NP reserva 25 kPa para tratamento de saída. Todas as peças passam no cenário, com pressão disponível de pelo menos **119,351 kPa**; especificação mínima adotada de 100 kPa para peças potáveis e 50 kPa para as caixas NP. Velocidades calculadas abaixo de 2 m/s, alvo de projeto.
- Aquecedor de acumulação 200 L/3 kW, armazenamento a 60 °C e mistura a 40 °C com limite de uso corporal de 45 °C. Para 200 L/dia misturados, são necessários 100 L/dia a 60 °C na hipótese de entrada a 20 °C. Aquecer os 200 L integrais de 20 para 60 °C exige 9,302 kWh e 3,101 h a 3 kW, sem perdas térmicas.
- Expansão de aproximadamente 3,05 L: vaso potável de 18 L possui capacidade calculada de 4 L entre as pressões adotadas de 250 e 350 kPa manométricos. Termostato/limitador independentes, misturador e grupo de segurança com alívio até 400 kPa, compatíveis com PMTA/fabricante, sem registro isolando a proteção. Selecionar conjunto certificado, isolamento e suportes apropriados.

### Esgoto e ventilação

Total de 27 UHC. Bacias DN 100; lavatórios/chuveiros DN 40; pia/tanque/lavadora DN 50; saídas CS DN 75; coletores DN 100. Declividades adotadas: 2% para DN menores que 100 e 1% para DN 100.

**A saída da pia foi refeita:** segue pela cozinha até CG1 externa em (105,310) mm da maquete, afastando o trajeto da sala. CG1 com volume útil mínimo de estudo de 18 L; CI com dimensão útil de 600 × 600 mm como escolha, tampas acessíveis. Definir bases/cobertura conforme cargas e profundidade.

As cotas são do fundo interno da tubulação, relativas ao piso 0,00 m. CI1 saída -0,300 m; CI2 -0,400 m; CI3 -0,375 m; CIE -0,500 m. A tubulação chega à fronteira DS1 a -0,506 m, acima da conexão de estudo a -0,600 m. Todas as chegadas são iguais ou superiores à saída da respectiva caixa. **A cota pública e o lote são hipóteses; se a rede real estiver mais alta, esse resultado perde validade.**

Os ralos H10/H11 têm ramais sem acrescentar novas UHC de consumo. Fechos hídricos nos desconectores, sem dupla sifonagem em série; bacias não atravessam CS. Tomadas de ventilação junto aos desconectores e nos ramais de bacias antes das CI; DN 50, comprimento de projeto até 10 m, cinco terminais a 5,30 m (mais de 2 m sobre a cobertura 3,18 m do modelo). O CAD inclui as subidas e conexões altas; suportes, peças e distâncias finais precisam de detalhamento. Observar retorno de condensado, captação de ar e aberturas.

### Chuva e não potável

Área de projeção de cobertura de 85,756 m². Chuva de projeto **adotada** de 180 mm/h, sem afirmar que corresponde à IDF/recorrência do lote. Vazão 4,288 L/s; com margem de 20%, 5,145 L/s.

Calha semicircular DE 200, lâmina de 80 mm, declividade 0,5%, n de Manning 0,011: capacidade 9,236 L/s. Ponto alto central e duas meias-calhas de 7,175 m, queda de 35,875 mm por lado. Duas descidas DN 100, uma para cada 42,878 m²: pré-seleção pelo critério simplificado do Manual Tigre. **Confirmar o ábaco de condutor, bocais, obstrução e extravasão no detalhamento executivo.** Coletor pluvial DN 150 a 1% passa na verificação de Manning a meia seção. Destinação legal independente do esgoto sanitário.

Desvio inicial hipotético de 2 mm = 171,512 L; recipiente adotado de 200 L. Tela/desvio devem admitir pelo menos 5,145 L/s. Cisterna com sedimentação, acesso e proteção contra insetos; tratamento na saída NP dimensionado por desempenho mínimo de 1,10 m³/h e perda máxima de 25 kPa, com bloqueio por falha. Filtração/desinfecção deve ser validada para a qualidade de entrada e para os usos definidos, sem declaração de eficácia laboratorial nesta revisão.

Reposição potável no sistema NP por separação atmosférica de estudo de 50 mm para bocal de até 20 mm acima do extravasor; nunca ligação direta entre as duas redes. Identificação e restrição de uso, limpeza, controle de qualidade, extravasor e acesso são requisitos. Não usar NP para higiene pessoal, preparo de alimentos ou consumo.

## Referências e alcance

- ABNT NBR 5410:2004, versão corrigida 2008, consultada para capacidade de corrente, PE, proteção, queda e banhos por [cópia acadêmica da PUC Goiás](https://professor.pucgoias.edu.br/SiteDocente/admin/arquivosUpload/18451/material/nbr_5410.pdf). Texto integral não copiado para o GitHub.
- [Manual Técnico Tigre](https://tigresite.s3.amazonaws.com/2021/10/Manual-Tecnico-Tigre.pdf), capítulos de consumo e esgoto/pluviais e apêndices: dados de referência de consumo e UHC/diâmetros e método simplificado de condutor. É manual de fabricante anterior à revisão 2020 da NBR 5626; os cálculos de AF/AQ desta entrega usam vazões explícitas e Darcy, sem declarar atualização do manual ou reproduzir suas tabelas integrais.
- [PBQP-H / manual setorial de instalação, uso e manutenção de metais sanitários](https://pbqp-h.mdr.gov.br/wp-content/uploads/2021/09/MANUAL_Intalacao-Uso-Operacao-Manutencao.pdf), seção de pressões/temperaturas, referenciando NBR 5626:2020. Consulta do conteúdo indexado; a abertura integral foi bloqueada pelo servidor. Não se afirma auditoria do texto integral dessa norma.
- [Enel SP, geração distribuída e normas de referência](https://www.enel.com.br/pt-saopaulo/Corporativo_e_Governo/geracao-distribuida.html) e [documentação necessária](https://www.enel.com.br/pt-saopaulo/Corporativo_e_Governo/geracao-distribuida/canais-de-atendimento/documentacao-necessaria.html): condições e documentos de acesso; não há solicitação ou aprovação de conexão.
- [Senado Verde](https://www.gov.br/compras/pt-br/agente-publico/logistica-publica-sustentavel/materiais-de-apoio/biblioteca-digital/edificios-publicos-sustentaveis-programa-senado-verde-2012.pdf) e [CAESB PR-14/2023-DC](https://s3.caesb.df.gov.br/www/prod/site1/2024/07/PR-14-2023-DC-Sistema-aproveitamento-agua-nao-potavel.pdf): concepção de separação NP; a referência do DF não é tratada como regra local deste lote.

Consulta em 06/11/2026. A R02 é um cenário calculado e auditável para o trabalho acadêmico. Não declara conformidade integral ou responsabilidade técnica de obra. Antes de qualquer execução real, é necessário rever os itens externos acima e as edições/regras locais aplicáveis com profissional habilitado.

## Reproduzir e conferir

Python 3, `reportlab`, `ezdxf`, DejaVu Sans e os arquivos R01 publicados são necessários. Na raiz do repositório:

```sh
python 06_Calculos/Dimensionamento_R02/Calcular.py
python 06_Calculos/Dimensionamento_R02/Testar_Dimensionamento.py
python 06_Calculos/Dimensionamento_R02/Gerar_Entregas.py
```

Dez grupos de testes verificam equilíbrio, coordenação/queda, correção C6, aquecimento/expansão, vazões/perdas/pressões, cotas/UHC, chuva/reservação e compatibilidade numérica da geração. Não substituem medição ou validação de fabricante. Os CSV/JSON registram arredondamentos; o código mantém maior precisão no cálculo.
