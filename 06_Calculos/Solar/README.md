# A06 | Estudo do experimento solar

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026.

O inventário informa painel de **12 V nominal, 125 mA e 1,5 W**, controlador sem modelo e bateria descrita como **12V 7A**. A última descrição não confirma capacidade em Ah, química ou regime admissível. Não foi calculada autonomia real dessa bateria.

O programa `solar.py` estima energia com premissas explícitas e não controla carga/descarga. Utiliza Python 3, sem biblioteca externa. Exemplo de estudo, com HSP e fator escolhidos apenas para demonstrar a conta:

```sh
python solar.py --hsp 4 --fator 0.75 --carga-w 1
python -m unittest teste_solar.py
```

Nesse exemplo hipotético, `1,5 W × 4 h × 0,75 = 4,5 Wh/dia`. HSP significa horas de sol pleno equivalentes; não é simplesmente o tempo em que existe claridade. Os valores 4 e 0,75 não representam medição ou condição confirmada do local.

Para estudar bateria, o programa só aceita o conjunto completo `--bateria-v`, `--bateria-ah`, `--dod` e `--eficiencia`. A fração utilizável e a eficiência são hipóteses de estudo, a fundamentar no fabricante e no circuito escolhido. Não preencher `--bateria-ah 7` apenas porque o inventário escreve 7A.

## Antes de integrar o circuito

Identificar painel, controlador e bateria pelas etiquetas/datasheets. Conferir compatibilidade entre tensão do painel em operação e em vazio, entrada/algoritmo do controlador, química/tensão de carga da bateria, cargas, proteções e conectores. O rótulo 12 V dos componentes não comprova que o conjunto carregue corretamente.

O experimento permanece separado da alimentação principal da maquete. A ficha `Registro_Solar.csv` está vazia para medições reais. Não há ensaio de carga, autonomia ou economia concluído. A parte de medição e as ligações serão detalhadas depois da identificação dos modelos e instrumentos disponíveis.
