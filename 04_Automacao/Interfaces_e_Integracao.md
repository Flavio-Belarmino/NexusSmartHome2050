# Interfaces e integração futura

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026.

Os programas de bancada preservam os pinos já propostos na R02. São ensaios separados. A matriz abaixo não declara que todas as funções já operem simultaneamente.

| Módulo | Entradas | Saídas nesta revisão | Integração ainda necessária |
| --- | --- | --- | --- |
| A01 iluminação | PIR D35, LDR A0 | Um LED L01 D22 | Demais zonas, comandos e supervisão unificada |
| A02 brise | LDR A0 e comandos USB | Sinal de servo D6, habilitado pelo operador | Fonte e curso físico; compartilhar a leitura do LDR com A01 |
| A03 acesso | RC522 SPI D49 a D53 | LED da placa indicando decisão | Driver/solenoide 6 V; D7 permanece sem acionamento |
| A04 ambiente | DHT22 D34 | Telemetria JSON USB | Política ambiental e atuadores se definidos |
| A05 água | HC-SR04 D10/D11; D2 reservado à vazão | Telemetria e LED de permissão lógica | Vazão/interface/calibração, driver e bomba; D8 sem acionamento |
| A08 comandos | Botões D40 a D43; parada lógica D3 | LEDs D22 a D32 | Estados gerais, prioridades e corte físico de atuadores |
| A07 garagem | Sensores virtuais na simulação | Comandos virtuais abrir/fechar | Mecanismo, sensores, pinos próprios e driver ainda não definidos |
| Supervisor USB | Quadros recebidos pelo computador | Tela local e CSV | Transporte Mega/ESP32 e rede depois de identificar a placa |

## Regras para a revisão integrada

- Um único proprietário para cada saída. A01 e A08 não podem escrever os mesmos LEDs em rotinas independentes sem uma camada que resolva modo e prioridade.
- Uma única aquisição do LDR, compartilhada entre iluminação e brise, com calibração registrada.
- Parada e falhas precedem comandos automáticos. O retorno da alimentação ou do contato de parada não deve acionar cargas inesperadamente.
- Tempos por `millis()` para tarefas cooperativas. A leitura ultrassônica atual bloqueia por no máximo 25 ms no ensaio isolado; avaliar captura não bloqueante ao integrar.
- A biblioteca Servo utiliza temporizadores; conferir os recursos e canais PWM antes de atribuir outros mecanismos. Não reaproveitar pinos por tentativa.
- Alimentações dos atuadores são separadas conforme o projeto, com referências e interfaces compatíveis. Sinal lógico e corrente de potência são funções distintas.
- Telemetria deve identificar módulo, validade, origem e tempo. Não exibir demonstração ou dado antigo como medição atual.

O supervisor preparado nesta revisão usa o USB do computador, apenas para leitura. Isso não é ainda a integração Wi-Fi/IoT ou Smart Grid da residência exigida no roteiro BLUEPRINT.
