# Verificação da hidráulica R01

Data: 05/11/2026. Conferências de documentação e cálculo.

| Conferência | Resultado |
| --- | --- |
| Referências de aparelhos/ralos | 11 centros dentro dos polígonos corretos e fora do setor de giro das portas do desenho R02 |
| Redes de abastecimento | 7 aparelhos com AF, 5 com AQ e 2 com NP; destinos NP sem alimentação AF/AQ direta |
| Cobertura | Contorno R02 com recuo: 85,756 m²; sem garagem |
| Cálculos | 4 testes passaram: unidades, evento seco/perdas totais, entradas inválidas e geometria/separação |
| PDF | Quatro páginas A3 renderizadas e inspecionadas visualmente; identificações de caixas separadas das referências de ralos |
| HPR01_Agua.dxf | 100 entidades; 0 erros e 0 correções na auditoria ezdxf |
| HPR02_Esgoto_Ventilacao.dxf | 108 entidades; 0 erros e 0 correções na auditoria ezdxf |

A conferência dos centros não verifica o tamanho de louças ou folgas de uso. Rotas, DN, cotas, declividades, ventilação, vazões, perdas de carga, tratamento e reservação permanecem para dimensionamento. O circuito físico de água não foi ensaiado.

## SHA-256 dos artefatos verificados

```text
7aa2f7e68955374c8205c1da82042936f8976a2ef760570cf34dc40290f649a4  Gerar_Estudo.py
201f05e058a2e84bee0b4f84b7543420ad1e997be397b766df870d3db0c9b118  Testar_Calculos.py
543cdf2728f824198984fb9cd4e8fde5fae4f38a7fbd26a771c8ee1383d4d1f4  NEXUS_Hidraulica_Residencial_R01.pdf
dbee876249d5bd89e45a602ed5d6ee0514a47b81cd1dbb9261da4b83647667aa  HPR01_Agua.dxf
6360bbec3b19f734e0fd51ca80f746f5b8f2752a837755334bd0a668443214bb  HPR02_Esgoto_Ventilacao.dxf
240f45baf4e0850daf8139d9b5a5f117b44d9699b0cfee99c90bf5cc464b929d  Pontos_Hidraulicos_mm.csv
0a5c91fa445438a2f19bae4897b903c43c3d27ae5501413cf99252cb8d342e30  Rotas_Propostas_mm.csv
33b53d4c78333d2aba61009b528055868c893bd478c9cbbf7c52f0f0b00bc0da  Cenarios_Chuva.csv
8ace4de02d7d95dc026d9ccce4c9a2aa55ca078b2d0b580116c4e946eb9620fe  Modelo_Hidraulico_R01.json
```
