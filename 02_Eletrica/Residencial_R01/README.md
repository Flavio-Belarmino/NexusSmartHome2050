# Elétrica residencial R01

Casa Inteligente | NEXUS | ExpoTech. Revisão de 05/11/2026, anterior à montagem. Este estudo usa a geometria e as dimensões de trabalho da R02.

## O que consultar

| Arquivo | Conteúdo |
| --- | --- |
| [PDF de quatro pranchas](NEXUS_Eletrica_Residencial_R01.pdf) | Iluminação e comandos; tomadas e reservas; ambientes/cargas; circuitos/equipamentos |
| [Iluminação em DXF](EPR01_Iluminacao.dxf) | Pontos e relações de comando, em milímetros arquitetônicos |
| [Tomadas em DXF](EPR02_Tomadas.dxf) | Tomadas, quadro proposto e reservas |
| [Ambientes e cargas](Ambientes_Cargas.csv) | Dimensões adotadas, áreas, perímetros e previsão por ambiente |
| [Coordenadas dos pontos](Pontos_Residenciais_mm.csv) | Identificação, parede, coordenadas e alturas nos dois modelos |
| [Circuitos](Circuitos_Propostos.csv) | Sete circuitos iniciais e corrente de estudo |
| [Reservas](Reservas_Equipamentos.csv) | Equipamentos propostos, ainda sem potência/circuito definidos |
| [Modelo JSON](Modelo_Eletrico_Residencial_R01.json) | Dados e premissas desta revisão |
| [Gerador](Gerar_Previsao.py) | Fonte reproduzível dos desenhos e tabelas |
| [Verificação](Verificacao_R01.md) | Conferências de geometria, cálculos e legibilidade |

Há **11 pontos de luz, 11 posições de comando e 28 tomadas de uso geral**. A previsão é de **1.240 VA de iluminação + 6.800 VA de TUG = 8.040 VA**. Não inclui as reservas de equipamentos nem a garagem. Não é demanda de entrada, potência final instalada ou consumo em kWh.

## Premissas e leitura

As coordenadas arquitetônicas são as coordenadas locais da maquete multiplicadas por 20, em mm. Não incluem a translação da casa na base de exposição. As cotas são estimativas do anteprojeto. A parede gráfica ampliada de 60 mm não especifica uma vedação residencial real. A área interna calculada pelos polígonos é 75,6632 m².

A hipótese de alimentação de C1 a C7 é 127 V. As correntes mostram apenas I = S/U; não selecionam disjuntores nem cabos. As reservas em 127/220 V ainda dependem da escolha dos equipamentos e do fornecimento.

Os pontos ficam na linha das paredes. As alturas propostas estão no CSV, não são apresentadas como mínimos normativos. No PDF, R06/R07 têm chamadas afastadas para leitura. No DXF, a altura dessas reservas aparece no texto. Os tracejados de comando no PDF e as linhas de comando no DXF ligam interruptores a luzes; **não representam trajetos de eletrodutos**. A simbologia é de estudo, com legenda própria.

A distribuição depende da compatibilização com mobiliário e instalações. As tomadas dos banhos pressupõem lavatórios ainda propostos; falta definir chuveiros e verificar seus volumes. A cozinha tem dois pontos acima de uma bancada proposta. Nada disso é registro de montagem ou aprovação para execução.

Os critérios de previsão foram conferidos na ABNT NBR 5410:2004, versão corrigida 2008, itens 9.5.2 e 9.5.3. Foi mantida a previsão de 600 VA nos três primeiros pontos dos ambientes pertinentes, sem a redução facultativa. A edição foi consultada no [catálogo oficial ABNT](https://abntcatalogo.com.br/default.aspx) em 05/11/2026. O texto normativo foi consultado em cópia acadêmica hospedada pela PUC Goiás; não é redistribuído neste repositório. Os resultados e sua aplicação estão nas tabelas e no código.

## Próxima etapa técnica

Definir o programa de equipamentos: cocção, forno, lavadora, aquecimento de água, climatização, central de rede/automação e garagem. Cada reserva precisa de potência, tensão, modo de instalação e características de operação. Esses usos são propostas, não compras obrigatórias para a maquete.

Depois: estabelecer fornecimento e condições de instalação; calcular demanda, distribuir cargas, dimensionar alimentador/condutores/proteções e queda de tensão; apresentar quadro/unifilar, aterramento, DR/DPS e entrada renovável. O detalhamento de automação também deve identificar interfaces e eventual comando manual. **Essas partes não estão concluídas nesta R01.**

A maquete segue com seus circuitos DC. As tensões residenciais do estudo não devem ser aplicadas ao Mega ou aos sensores.

## Reproduzir

Na raiz do repositório, com Python 3, `reportlab` e `ezdxf` instalados:

```sh
python 02_Eletrica/Residencial_R01/Gerar_Previsao.py
```

O gerador usa os arquivos JSON/CSV publicados em `01_Arquitetura/R02/DADOS`. A fonte DejaVu Sans é procurada em `/usr/share/fonts/truetype/dejavu`; adaptar `setup_fonts` se o sistema usar outro caminho. A geração valida posições e somatórios antes de escrever o PDF. Datas e identificadores internos do PDF/DXF podem variar entre execuções.
