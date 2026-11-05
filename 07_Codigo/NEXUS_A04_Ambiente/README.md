# A04 | Temperatura e umidade

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026. Monitoramento com DHT22/AM2302 e Mega. Não comanda climatizador, ventilador ou outro atuador.

## Material e ligações
Mega/USB, DHT22, jumpers e resistor de 10 kΩ caso o sensor não tenha o pull-up incorporado. Conferir se é o sensor avulso de quatro pinos ou módulo montado de três pinos.

| Função do sensor | Mega |
| --- | --- |
| VCC, em módulo identificado como compatível | 5V |
| GND | GND |
| DATA / sinal | D34 |
| Pull-up, quando necessário | 10 kΩ entre DATA e VCC |

No sensor de quatro pinos há uma posição não conectada. Identificar pelo datasheet ou marcação antes de ligar; a tabela não representa uma ordem física dos terminais. Não acrescentar ou retirar resistor por suposição se a placa tiver componentes montados.

## Software
Instalar **DHT sensor library**, da Adafruit, e sua dependência **Adafruit Unified Sensor**. Versões compiladas: 1.4.7 e 1.1.15, respectivamente. Abrir `NEXUS_A04_Ambiente.ino`, selecionar Mega/ATmega2560, carregar e abrir Monitor Serial a 115200.

O programa lê a cada **2,5 segundos**. Mostra temperatura em °C, umidade relativa em % e `valid`. Quando uma leitura falha, apresenta `null` nos dois valores e incrementa `consecutive_failures`; não transforma falta de leitura em temperatura zero.

## Testar
1. Aguardar leituras estáveis e guardar uma sequência de pelo menos um minuto.
2. Comparar com instrumento de referência, se disponível, registrando as condições. Sem referência, registrar apenas consistência e repetibilidade, sem alegar exatidão medida.
3. Verificar falha de leitura com o circuito desligado para alterar a conexão e posterior retorno à condição normal. Não molhar ou aquecer diretamente o sensor.
4. Guardar a saída JSON, data e foto das ligações. A leitura pode ser vista no supervisor USB preparado para estes módulos.

Referências: [guia de ligação Adafruit](https://learn.adafruit.com/dht/connecting-to-a-dhtxx-sensor); [biblioteca e dependências](https://github.com/adafruit/DHT-sensor-library). Compilação concluída; ensaio físico pendente.
