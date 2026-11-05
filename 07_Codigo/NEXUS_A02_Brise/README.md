# A02 | Brise: ensaio do servo e da luminosidade

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026. Programa de bancada para Mega, separado dos demais sketches. Não é firmware integrado. Primeiro testar o servo livre, sem ligação mecânica ao brise.

## Separar
Mega, cabo USB, microservo já reservado ao brise, LDR KY-018, jumpers e fonte externa **5 V DC regulada**, compatível com a corrente de pico que será conferida. Não usar o pino 5V do Mega para alimentar o servo neste procedimento. Utilizar uma fonte pronta para uso, sem fazer ligações na rede elétrica.

## Ligações por função
| Origem | Destino |
| --- | --- |
| Sinal do servo | Mega D6 |
| Positivo de alimentação do servo | +5 V da fonte externa |
| Negativo do servo | GND da fonte externa |
| GND da fonte externa | GND do Mega |
| KY-018 S / + / − | Mega A0 / 5V / GND |

Conferir função dos fios do servo e marcações do LDR; não depender só das cores. Manter o +5 V da fonte do servo separado do pino 5V do Mega. Fazer ligações com as duas alimentações retiradas.

## Programa e passos
Instalar **Servo**, da Arduino, pelo gerenciador de bibliotecas. Versão usada na compilação: 1.3.0. Abrir `NEXUS_A02_Brise.ino` na pasta de mesmo nome, selecionar Mega/ATmega2560 e carregar. Monitor Serial em **115200**.

1. Ao ligar, o programa não emite sinal de servo. Conferir novamente as alimentações.
2. Com o servo livre, enviar `i`. Ele recebe o comando inicial de 90°. Pode se movimentar imediatamente até essa posição.
3. Usar `<` para 60°, `n` para 90° e `>` para 120°. O deslocamento de comando ocorre em passos de 1° a cada 25 ms.
4. Expor o LDR à condição clara, esperar leitura estabilizar e enviar `c`. Cobrir, esperar estabilizar e enviar `e`. Exigir separação de pelo menos 80 unidades ADC.
5. Enviar `a` para o automático. Nesta associação inicial, claro pede 120° e escuro pede 60°. Isso ainda não define abrir/fechar o brise físico: o sentido será conferido com o mecanismo.
6. `x` retira o sinal de comando; não corta a alimentação nem garante a sustentação da posição. Desconectar a fonte para desenergizar.

O campo `angle_command_deg` informa o ângulo solicitado pelo programa, não uma posição medida por sensor. O servo do inventário não tem retorno externo de posição confirmado.

## Registrar
Verificar inicialização, três posições livres, sentido, estabilidade da fonte, corrente/pico quando houver instrumento adequado e comportamento do automático. Só acoplar ao brise depois de conferir curso e esforço; os limites de 60° a 120° são de bancada. Preencher a ficha desta pasta com resultado real.

Referências: [biblioteca Servo](https://github.com/arduino-libraries/Servo); [KY-018 Joy-IT](https://sensorkit.joy-it.net/en/sensors/ky-018); pinagem NEXUS R02. Compilação registrada no índice geral; ensaio físico pendente.
