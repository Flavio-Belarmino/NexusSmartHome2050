# A05 | Água: nível, pulsos e permissão lógica

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026. A primeira etapa mede distância com HC-SR04 e testa a decisão de permitir uma bomba. **O programa não liga a bomba: D8 permanece como entrada.** O LED da placa mostra apenas a permissão lógica.

## Primeiro ensaio, sem água e sem bomba
Mega alimentado por USB, HC-SR04 e jumpers. Ligar VCC em 5V, GND em GND, TRIG em **D10** e ECHO em **D11**, conferindo as marcações. Manter bomba, fonte de 12 V e drivers desconectados.

Abrir o `.ino` com `controle_agua.h` na mesma pasta. Não há biblioteca externa. Selecionar Mega/ATmega2560 e Monitor Serial 115200. O disparo ocorre a cada 200 ms e a espera de eco é limitada a 25 ms. Distância sem eco válido aparece como `null`.

1. Usar um alvo plano e conferir a distância com uma régua. Primeiro validar a leitura em bancada.
2. Colocar o alvo na distância que representará o reservatório vazio e enviar `v`.
3. Colocar o alvo na distância de cheio e enviar `c`. A distância de vazio deve ser maior que a de cheio, com diferença mínima de 2 cm, e ambas dentro da faixa de leitura do ensaio.
4. Mover o alvo para um nível intermediário e enviar `p`. O LED só pode acender com calibração aceita, nível válido e pelo menos 20% da altura útil.
5. Levar a representação abaixo de 20% ou retirar o eco: a permissão cai e a falha fica retida.
6. `r` rearma e cancela o pedido anterior. Um novo `p` é necessário. `0` cancela o pedido normalmente.

Os 20% e 4 segundos de ausência de fluxo são parâmetros iniciais de estudo. O percentual é de **altura útil**, não volume medido, especialmente se o reservatório tiver seção variável. A calibração se perde ao reiniciar.

## Sensor de vazão: preparação
O inventário não identifica suficientemente a saída elétrica nem o fator de pulsos. Por isso, `VAZAO_CONFIRMADA=false` e `PULSOS_POR_LITRO=0` na versão publicada. A saída informa `flow_enabled=false` e `flow_l_min=null`.

Antes de habilitar D2, identificar modelo, alimentação, saída e necessidade de pull-up/interface. A tensão de saída para o Mega deve ser compatível com sua entrada; não ligar uma saída de 12 V ao pino. Medir o fator com recipiente graduado: **pulsos por litro = pulsos contados / litros de referência**. Repetir em condições registradas antes de usar o fator.

Com a vazão habilitada e calibrada, o programa conta pulsos por interrupção em D2 e calcula a média da janela. No pedido lógico de bomba, ausência de pulso por 4 segundos após a partida retém falha. Repetir `p` não deve renovar o prazo de proteção.

## Etapa física posterior
O acionamento real exige driver, proteção de carga indutiva, fonte compatível, proteção elétrica e teste da bomba em bandeja. O teste de distância no alvo não comprova a leitura sobre água, espuma, superfície inclinada ou dentro do recipiente escolhido. Não deixar o sensor e as conexões se molharem.

Referências: [datasheet HC-SR04](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf), pinagem e inventário NEXUS R02. A lógica tem testes em computador; nível, fluxo e bomba ainda não foram ensaiados fisicamente.
