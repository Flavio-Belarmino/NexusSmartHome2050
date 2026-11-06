# Hidráulica residencial R01

Casa Inteligente | NEXUS | ExpoTech. Distribuição esquemática de 05/11/2026. A geometria R02 foi preservada. Esta revisão avança o desenho das instalações antes da montagem; não conclui o dimensionamento exigido para a entrega final.

| Arquivo | Conteúdo |
| --- | --- |
| [Quatro pranchas em PDF](NEXUS_Hidraulica_Residencial_R01.pdf) | Água fria/quente/não potável; esgoto/ventilação; chuva e automação; coordenadas e continuidade |
| [Água em DXF](HPR01_Agua.dxf) | Rotas por camada e pontos de referência, em mm arquitetônicos |
| [Esgoto e ventilação em DXF](HPR02_Esgoto_Ventilacao.dxf) | Percursos propostos, inspeções e ventilação funcional |
| [Pontos em CSV](Pontos_Hidraulicos_mm.csv) | Centros de referência nos dois modelos, aparelhos e redes |
| [Rotas em CSV](Rotas_Propostas_mm.csv) | Vértices, origem/destino e comprimento em projeção |
| [Modelo JSON](Modelo_Hidraulico_R01.json) | Premissas, pontos, nós, percursos e cobertura |
| [Cenários de chuva](Cenarios_Chuva.csv) | Exemplos de volume por evento, com hipóteses explícitas |
| [Código gerador](Gerar_Estudo.py) | Fonte reproduzível dos desenhos e tabelas |
| [Conferências de cálculo](Testar_Calculos.py) | Unidades, limites e rejeição de parâmetros inválidos |
| [Registro de verificação](Verificacao_R01.md) | Conferências e limites dos resultados |
| [Preparação da bancada](Preparacao_Ensaio_Agua.md) | O que separar, conferir e testar antes de fixar a instalação |

## O que foi proposto

São **11 referências de aparelhos/ralos**, todas dentro dos ambientes R02 e fora do setor de giro das portas representado no modelo. Sete aparelhos recebem água fria potável (AF), cinco também recebem água quente (AQ), e duas bacias recebem água não potável (NP) proveniente de chuva tratada, como proposta de projeto.

As coordenadas são centros de referência para organizar o layout. Não são dimensões de louças nem eixos de conexão. Ainda precisam de modelos dos aparelhos, folgas de uso, acessibilidade, cotas e alturas. Os círculos no PDF e no CAD são símbolos identificadores. No DXF de água os ralos também aparecem como referências, sem ramais de abastecimento.

A conversão usa o fator 20 da R02. A origem é local às paredes; não inclui o deslocamento da casa na base de exposição. A representação de paredes de 60 mm não define o sistema construtivo real.

Os **38 percursos** são esquemáticos. Comprimentos em projeção não incluem todas as subidas, descidas, conexões ou folgas; trechos compartilhados aparecem em mais de um percurso. **Não somar esses comprimentos para comprar tubos.** Não foram definidos diâmetros nominais (DN), declividades, pressões, cotas de fundo ou dimensionamento de caixas.

AF distribui água para pia, lavatórios, chuveiros, tanque e lavadora, além da alimentação proposta do aquecimento AQ1. A distribuição AQ atende pia, lavatórios e chuveiros. Fonte de energia, temperatura, vazão, potência, retorno e proteções do aquecimento estão abertos. Isso exige compatibilização com a reserva elétrica R04, sem adicionar uma carga por suposição.

A rede NP atende apenas as descargas H03/H06 nesta revisão, sem ligação direta a AF/AQ. Reposição por água potável, quando necessária, deverá usar solução com separação atmosférica a projetar. Qualidade, tratamento, operação e identificação da rede precisam ser definidos. O esquema não autoriza consumo da água nem operação de instalação real.

Esgoto: pia direcionada à função CG1, banhos à desconexão/coleção CS1/CS2, bacias diretamente ao percurso sanitário sem atravessar as caixas sifonadas. Tanque/lavadora precisam de desconexão detalhada. CI1/CI2 representam inspeções e VT1/VT2 funções de ventilação, sem dimensionamento ou terminal executivo. A saída sanitária DS1 depende do lote e da concessionária. Chuva não foi conectada ao esgoto sanitário.

**Interferência já identificada:** o percurso proposto H01-CG1 cruza a projeção da sala sob o piso. Conferir estrutura, fundações e manutenção, ou adotar outra rota. A planta ainda não comprova que o esgoto consegue escoar por gravidade.

## Cobertura e cálculo de chuva

O contorno R02 foi convertido para a mesma origem das paredes, incluindo o recuo central. A área de projeção é **85,756 m²**, sem garagem. Calha e caimentos desenhados são propostas a verificar; a área efetivamente conectada ainda depende de compatibilização com cobertura e solar.

Por conversão de unidades, 1 mm sobre 1 m² equivale a 1 litro. O cálculo usado é `V(L) = P(mm) × A(m²) × C × eficiência`. C e eficiência são fatores adimensionais de estudo, não valores normativos adotados por material.

Com 10 mm hipotéticos: 857,56 L antes das perdas. Com C = 0,80 e eficiência = 0,90 hipotéticos: 617,443 L. Não há série histórica local, consumo definido ou balanço de reservação. Esses números **não dimensionam a cisterna, não são autonomia e não comprovam economia**. Desvio inicial, tratamento, excedentes, intensidade de projeto e condutores ainda precisam ser calculados.

A escolha de chuva para descargas é uma proposta de escopo. Não foi acrescentado tratamento de água cinza nesta revisão. Não existe comprovação de captação física, tratamento ou qualidade de água na maquete.

## Integração com elétrica e automação

Verificar os volumes finais dos chuveiros em relação aos pontos elétricos, incluindo T09/T24. Compatibilizar pia/bancada H01 com T05/T06 e lavadora H09 com a reserva R03 e T12. A bomba NP e o aquecimento precisam de características reais antes de revisar as cargas elétricas.

O módulo [A05 de bancada](../../07_Codigo/NEXUS_A05_Agua/) mede e decide uma permissão lógica. **D8 está configurado como entrada e não aciona bomba.** Fluxo permanece desabilitado até identificar a interface e calibrar o sensor. A proposta de circuito fechado de bancada não substitui as redes prediais nem demonstra tratamento. Veja a [preparação do ensaio](Preparacao_Ensaio_Agua.md).

## O que falta para dimensionar

Definir população e consumo, aparelhos/vazões, pressões, fonte de abastecimento, materiais, aquecimento, reservatórios/cotas, estrutura, implantação do lote, chuva local e destinação sanitária/pluvial. Em seguida: memória de cálculo, diâmetros, perdas de carga, temperaturas, cotas/declividades, ventilação, tratamento, armazenamento, bombeamento e quantitativos consolidados.

O roteiro BLUEPRINT pede redes fria/quente, esgoto/ventilação e captação/reúso. Esta revisão atende à preparação gráfica inicial dessas frentes; **o nível executivo ou esquemático dimensionado ainda não está concluído**.

## Referências consultadas e limites

- [Roteiro BLUEPRINT 2026.2, p. 1](../../10_Documentacao/Regulamento/Roteiro_BLUEPRINT_2026_2.pdf): escopo da entrega de hidráulica.
- [Senado Verde, Edifícios Públicos Sustentáveis, pp. 30-32](https://www.gov.br/compras/pt-br/agente-publico/logistica-publica-sustentavel/materiais-de-apoio/biblioteca-digital/edificios-publicos-sustentaveis-programa-senado-verde-2012.pdf): referência conceitual de captação e separação de reservatórios/redes.
- [CAESB, PR-14/2023-DC, itens 4.2-4.8](https://s3.caesb.df.gov.br/www/prod/site1/2024/07/PR-14-2023-DC-Sistema-aproveitamento-agua-nao-potavel.pdf): referência técnica de separação, identificação e proteção contra retorno. É um documento do Distrito Federal; não foi tratado como exigência local para esta residência.
- Referências para a etapa de dimensionamento: ABNT NBR 5626 (água fria/quente), NBR 8160 (esgoto), NBR 10844 (pluviais) e NBR 15527 (aproveitamento de chuva). Confirmar edições vigentes, consultar os textos e as regras locais antes de aplicar critérios. Esta R01 não declara atendimento integral às normas.

As fontes externas foram consultadas em 05/11/2026 para os conceitos indicados. Seus documentos não foram copiados para o repositório.

## Reproduzir

Requer Python 3, `reportlab`, `ezdxf` e DejaVu Sans em `/usr/share/fonts/truetype/dejavu` (ajustar a função `fonts` em outro sistema). Na raiz do repositório:

```sh
python 03_Hidraulica/Residencial_R01/Gerar_Estudo.py
python 03_Hidraulica/Residencial_R01/Testar_Calculos.py
```

O gerador lê o JSON R02, valida centros/portas e separação dos destinos, e escreve o PDF, DXFs e dados na própria pasta. Datas/identificadores internos dos formatos CAD/PDF podem variar entre execuções.
