# Testes propostos para a garagem

**Estado: não executados.** Definir previamente tempos máximos, posições de referência, campo de detecção e condição física de parada. Associar cada resultado ao firmware e à montagem usados.

| ID | Condição a provocar | Resposta a verificar |
| --- | --- | --- |
| G01 | Ligar com posição desconhecida | Aguardar referência controlada, sem movimento automático cego |
| G02 | Aproximação externa e solicitação válida | Abrir e confirmar posição aberta |
| G03 | Aproximação interna e solicitação válida | Permitir a sequência de saída |
| G04 | Abertura sem passagem confirmada | Permanecer em espera, sem presumir travessia |
| G05 | Passagem confirmada com vão liberado | Fechar conforme sequência e intervalo definidos |
| G06 | Obstáculo durante fechamento | Interromper e reabrir conforme projeto |
| G07 | Posição não atingida no tempo máximo | Parar e indicar falha |
| G08 | Emergência ou sensor inconsistente | Entrar em condição de parada/espera definida e exigir rearme |
| G09 | Reinício e operação simultânea de outros módulos | Retomar estado conhecido sem movimento inesperado |

Para cada caso, preencher: código/commit, montagem, parâmetros, data, responsável, resultado observado, aprovação/reprovação, falha e foto/vídeo. A resposta prevista ainda precisa ser implementada e comprovada.
