# Potências conhecidas e limites do protótipo

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026. Valores de rótulo transcritos do inventário; não são medições desta montagem.

| Item | Dados disponíveis | Conta de referência |
| --- | --- | --- |
| Painel | 12 V nominal, 125 mA, 1,5 W | 12 × 0,125 = 1,5 W nominal |
| Bomba | 12 V, 0,5 a 0,7 A em regime informado | 12 × 0,5 a 12 × 0,7 = **6 a 8,4 W** |
| Fontes 12 V | 5 A cada, duas unidades no inventário | Capacidade nominal 60 W por unidade; não significa consumo permanente de 60 W |
| Fontes 5 V | 3 A cada, duas unidades | Capacidade nominal 15 W por unidade; conferir saída e condição de uso |
| Solenoide | 6 V, corrente ainda desconhecida | Potência e ciclo de uso ainda não calculados |
| Servo | Modelo 9 g, corrente/pico não identificados | Não dimensionar pela massa de 9 g; identificar especificação e medir quando possível |
| Fita LED | Comprimento comercial informado, tensão/corrente desconhecidas | Identificar antes de dimensionar alimentação e driver |
| Bateria | Descrição “12V 7A” | Não confirma capacidade em Ah, energia útil ou corrente admissível |

Mesmo comparando apenas os valores nominais, a bomba demanda de **4 a 5,6 vezes** a potência nominal do painel. O painel não sustenta essa bomba continuamente por ligação direta. Isso não define sozinho o tempo de operação com bateria: faltam consumo total, capacidade real, estado de carga, controlador e perdas.

Para energia ao longo do tempo, usar `E = P × t` com unidades coerentes. Para o painel, o estudo em `solar.py` depende de HSP e fator explicitamente assumidos. Não declarar autonomia ou autossuficiência a partir da tensão nominal de 12 V ou da potência máxima das fontes.
