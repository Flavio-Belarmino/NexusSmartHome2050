# Verificação R02

Casa Inteligente | NEXUS | ExpoTech. 06/11/2026.

## Resultado

Os dez grupos de testes de `Testar_Dimensionamento.py` passaram. Os testes percorrem os circuitos e trechos do modelo, verificando unidades, balanços e limites nas hipóteses declaradas. São verificações computacionais, sem ensaios físicos ou certificação normativa integral.

| Conferência | Resultado observado |
| --- | --- |
| Carga, ampacidade e queda | 20 circuitos de carga; Ib <= In <= Iz; queda total máxima 3,7023% |
| Serviço C6 | 2,5 mm² não atendia ao limite do cenário; adotados 4 mm² |
| Fases | 76,74 / 75,81 / 75,72 A, abaixo de 100 A no modelo fasorial |
| Alimentador | Ampacidade corrigida acima de 100 A; ocupação calculada abaixo de 40% |
| Aquecimento | Energia integral 9,302 kWh; expansão calculada menor que capacidade útil do vaso |
| Água | Balanço AF+AQ 1,15 L/s; NP 0,30 L/s; pressões acima dos requisitos de projeto |
| Esgoto | 27 UHC; cotas calculadas chegam acima da saída de cada caixa; CG1 revisada para exterior da cozinha |
| Chuva | Vazão 4,288 L/s; calha e coletor passam na margem de 20%; reservação NP supera seis dias do consumo adotado |
| Fotovoltaica | Potências/string, corrente admissível e quedas CC/CA verificadas no modelo; geração separada da carga |
| PDFs | Dois arquivos de seis páginas, A3 horizontal (1190,6 x 841,9 pt), com texto extraível em todas as páginas |
| Inspeção visual | As 12 páginas renderizadas foram conferidas quanto a margens, tabelas, desenhos e sobreposição aparente de textos |
| CAD | Quatro DXFs reabertos e auditados com ezdxf: nenhum erro e nenhum reparo automático |

Comandos executados a partir da raiz:

```sh
python 06_Calculos/Dimensionamento_R02/Gerar_Entregas.py
python 06_Calculos/Dimensionamento_R02/Testar_Dimensionamento.py
```

## Limites da verificação

Não foram medidos circuito de terra, impedância de laço, curto-circuito, pressão, chuva, cotas públicas ou consumo real. Não foram ensaiados equipamentos, bombas, aquecedor ou tratamento. As curvas dos fabricantes, energia passante/coordenação e tempos TT, NPSH, grupo de segurança e ábacos/bocais pluviais continuam como condições de seleção/detalhamento externo, descritas no README e nos cadernos.

Os testes não substituem revisão profissional nem convertem o cenário acadêmico em autorização de obra ou energização. A instalação DC e os ensaios de recirculação da maquete são sistemas separados.
