# Verificação da revisão elétrica R01

Data: 05/11/2026. Verificações de documentação e cálculo, sem ensaio físico.

| Conferência | Resultado |
| --- | --- |
| Áreas | Calculadas pelos polígonos; diferença em relação ao CSV R02 menor que 0,0006 m² por ambiente |
| Pontos de parede | Dentro do segmento; sem interseção com portas/janelas na altura proposta |
| Previsão de iluminação | 1.240 VA; fronteiras da fórmula verificadas em 6, 9,999, 10 e 14 m² |
| TUG | 28 propostas; quantidade proposta por ambiente igual ou superior ao mínimo calculado; 6.800 VA |
| Circuitos | Soma 8.040 VA; corrente de estudo igual a S/127, com tolerância de arredondamento de 0,0001 A |
| PDF | Quatro páginas A3; renderizadas e inspecionadas visualmente; chamadas R06/R07 separadas para leitura |
| EPR01_Iluminacao.dxf | 118 entidades; 0 erros e 0 correções na auditoria ezdxf |
| EPR02_Tomadas.dxf | 141 entidades; 0 erros e 0 correções na auditoria ezdxf |

Essas verificações não conferem volumes de banho, mobiliário, luminotécnica, dimensionamento, seletividade ou executabilidade das instalações. A garagem e as cargas das reservas estão fora do total.

## SHA-256 dos artefatos conferidos

```text
7a7d3d372b83da4236565c5c8c87bf40ce41ec379769b18b164d1ec4abd1b98d  Gerar_Previsao.py
265069a27ca471c4a894bf2041c20a413e99155aa1069650b5c18740d2cd453a  NEXUS_Eletrica_Residencial_R01.pdf
cdf22f7580a15482fee94c222a84458f7bd2e38deb83f8709e7f72358c193314  EPR01_Iluminacao.dxf
c0c5007cbd8b9bdfe38b84f39c776c39d4727a122919cb4039c36b5448e58767  EPR02_Tomadas.dxf
e1614cfd749a9a91e779d0dbe0c2eb33ce50b24e77d614b0a509fac8de3b627e  Ambientes_Cargas.csv
e61c5c973f388032bf92f063a05473ba89b87c098ba3fa981e5a4504553120cb  Circuitos_Propostos.csv
e8281c5edd3f0250cd0c5a014c37e7bbd379b038dd76eb090735021bc2454b7b  Pontos_Residenciais_mm.csv
d53873baf09c9d75b9dca48fdd4a66ee60106a10b7c3f1ef3886207f59ddb3e1  Reservas_Equipamentos.csv
c0b474d3f3b2b5b664b8403e008fbac16e6e6a008f2000fa201d188f0f9a6197  Modelo_Eletrico_Residencial_R01.json
```
