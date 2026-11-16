# NEXUS TFT integrado R06

Firmware de demonstração para **Arduino Mega 2560**, preservado conforme a revisão usada no desenvolvimento. Publicação documental em 16/11/2026. [Código integral](NEXUS_TFT_Integrado_R06.ino).

## Abrir e carregar

1. Instalar Arduino IDE e o pacote Arduino AVR Boards; selecionar Arduino Mega or Mega 2560 / ATmega2560 e a porta correta.
2. Instalar MCUFRIEND_kbv, Adafruit GFX Library, Adafruit TouchScreen, MFRC522, Servo, DHT sensor library e as dependências solicitadas (Adafruit BusIO e Adafruit Unified Sensor).
3. Abrir `NEXUS_TFT_Integrado_R06.ino` dentro da pasta de mesmo nome. Não adicionar os sketches A01-A09 a essa pasta.
4. Conferir a [pinagem CSV](../../04_Automacao/Pinagem_Mega_R06.csv) e o [guia PDF](../../10_Documentacao/Guias/NEXUS_Guia_Pratico_Pinagens_R06.pdf), com fontes desligadas durante a montagem.
5. Carregar o programa; Monitor Serial em 9600 baud. Para data/hora: enviar `H AAAA-MM-DD HH:MM:SS` com Nova linha.

[Regras completas](../../04_Automacao/Automacao_Integrada_R06.md). As cinco páginas são início, iluminação, garagem, água e clima. AUTO alterna a cada 3 s; comandos manuais pausam. Botões físicos de navegação: 25 e 26. Na tela clima, TESTAR aciona buzzer/LED por 3 s, PARAR interrompe e SILENCIAR cancela; o botão 24 também silencia.

## Parâmetros de demonstração

- Servo 30: 0°/90°, passo nominal de 10 ms por grau, 250 ms de acomodação. LED 33 acompanha o movimento. A animação visual é mais lenta que o servo e não mede posição.
- Botão do portão 32; comandos manuais mantêm a posição. RFID abre/fecha automaticamente após 3 s de espera; se já estiver aberto/abrindo, apenas fecha.
- UIDs de demonstração cadastrados no fonte: `86 60 71 9E` e `DA 76 FA 55`. Retirar e reapresentar o cartão/tag para novo comando.
- LDR A9, luz 34 ativa em LOW; água A8, LED 28; DHT 22, LED 23, buzzer 44, silenciar 24; relé 42 ativo em LOW e nível 43 com HIGH desligando a bomba.
- Alarme a partir de 30 °C; rearme abaixo ou igual a 29,5 °C. O relógio não conserva a hora após reinício, pois não há RTC.

## Validação e pendências

[Validação de software](Validacao_Software_R06.md) e [testes reproduzíveis](tests/teste_logica_r06.py). Requisitos do teste: Python 3 e g++ com C++11; executar `python3 tests/teste_logica_r06.py` nesta pasta. O teste usa entradas simuladas, sem afirmar precisão dos sensores ou esforço mecânico.

O alarme tem uma falha física relatada: a abertura NEXUS reaparece, indicando reinício do Mega. Causa ainda não identificada. Confirmar modelo/interface do buzzer e alimentação/acionamentos antes do ensaio final. A expiração do teste não resolve essa falha.

As funções de bancada tiveram relatos positivos da equipe; a R06 e a remontagem completa precisam de comprovação final. Sem sensores de obstáculo, passagem ou fim de curso; sem integração ESP32/Wi-Fi ou acionamento de climatização.
