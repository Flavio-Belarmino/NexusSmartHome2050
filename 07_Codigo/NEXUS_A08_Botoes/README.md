# A08 | Botões, iluminação e parada lógica

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026. Ensaio independente de LEDs, comandos locais e retenção de parada. Sem bomba, servo, solenoide, fita ou relé conectados.

## Ligações
Cada LED precisa do seu resistor em série, entre a saída e o ânodo; cátodo para GND. Os valores preservam a distribuição R02 e as quantidades do inventário.

| Canais | Pinos | Resistores individuais |
| --- | --- | --- |
| L01 a L05 | D22 a D26 | 5 resistores de 470 Ω |
| L06 a L10 | D27 a D31 | 5 resistores de 560 Ω |
| L11 | D32 | 1 resistor de 1 kΩ |
| Botões 1 a 4 | D40, D41, D42, D43 | Contatos normalmente abertos para GND; pull-up interno |
| Parada lógica | D3 | Contato normalmente fechado para GND; abertura do circuito bloqueia |

Identificar os contatos do botão de emergência antes de usar. Se ele não oferecer contato NC, não presumir equivalência. Só para este ensaio de LEDs, uma ponte removível D3-GND pode representar o contato fechado. Remover a ponte representa uma abertura. Isso não é uma parada física de potência.

## Programa e teste
Sem biblioteca externa. Carregar `NEXUS_A08_Botoes.ino` no Mega e abrir Monitor Serial 115200.

1. Inicia **bloqueado**, LEDs externos apagados. O LED da placa indica bloqueio.
2. Com D3-GND fechado, enviar `r` para rearmar. O fechamento do contato sozinho não rearma.
3. Enviar `t`: os 11 LEDs devem acender um por vez, por 300 ms, e terminar apagados. Conferir os canais na planta.
4. Apertar os botões 1 a 4: alternam L01 a L04. Os comandos `1`, `2`, `3`, `4` fazem o mesmo pelo computador. Há filtro de 30 ms para os contatos.
5. Abrir D3-GND durante o teste: todos os LEDs apagam e o bloqueio fica retido.
6. Fechar novamente e conferir que nada reinicia sozinho. Só então enviar `r`.
7. `0` apaga os LEDs. Se um comando manual interromper a sequência, ela é cancelada e as outras saídas da sequência são apagadas.

O programa testa a leitura e a decisão lógica. Um botão lido pelo Mega não substitui o corte físico independente da alimentação dos atuadores, que será projetado depois de identificar as cargas e os componentes de potência.

Referência: pinagem, circuitos e inventário NEXUS R02; funções `INPUT_PULLUP` e `digitalRead` da plataforma Arduino. Compilação concluída; ensaio físico pendente.
