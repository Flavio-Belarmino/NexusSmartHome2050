# Primeiro ensaio: iluminação na bancada

Casa Inteligente | NEXUS | ExpoTech. A01 R01, 05/11/2026.

Este ensaio é uma primeira etapa da programação. Usa **um LED**, o sensor PIR e o módulo LDR ligados ao Arduino Mega. Ainda não integra os demais sistemas da casa. O programa começa desligado e oferece comandos pelo computador para testar cada parte antes do automático.

**Situação:** firmware compilado para Mega/ATmega2560 e lógica aprovada em 28 verificações em computador; teste físico ainda pendente. A calibração depende dos sensores reais. O procedimento não exige que a casa esteja montada.

[Pacote ZIP deste ensaio](../NEXUS_A01_Bancada_R01.zip). Ao abrir a página do ZIP no GitHub, usar o botão de download; depois extrair a pasta antes de abrir o programa.

## Antes de montar qualquer ligação

Separem o Mega e o cabo USB, protoboard, jumpers, um LED branco, um resistor de **470 Ω**, o módulo de luminosidade KY-018 e o sensor de movimento. Todos constam do inventário.

Identifiquem as marcações dos conectores dos sensores. A tabela abaixo informa a função elétrica; não informa a posição esquerda/direita dos pinos. Existem placas com disposição diferente. Se a identificação não estiver clara, fotografem os dois lados do módulo para conferirmos antes de conectar.

Neste ensaio, usem a alimentação USB do Mega e apenas esses componentes. Os demais atuadores e fontes externas ficam desconectados. Façam e alterem as ligações com o USB retirado.

## Ligações

| Origem | Destino | Observação |
| --- | --- | --- |
| Mega D22 | Uma ponta do resistor de 470 Ω | É o pino L01 previsto na R02 |
| Outra ponta do resistor | Ânodo do LED | Terminal positivo, geralmente a perna mais comprida em LED novo |
| Cátodo do LED | GND do Mega | Terminal negativo; conferir também a face achatada do encapsulamento |
| PIR VCC ou + | 5V do Mega | Confirmar que é o módulo PIR compatível com essa alimentação |
| PIR GND ou − | GND do Mega | Terra comum |
| PIR OUT ou sinal | Mega D35 | Entrada prevista na R02 |
| KY-018 + ou VCC | 5V do Mega | Módulo de referência Joy-IT admite 3,3 a 5 V; conferir a placa recebida |
| KY-018 − ou GND | GND do Mega | Não deduzir a posição pela cor do fio |
| KY-018 S ou sinal | Mega A0 | Entrada prevista na R02 |

O resistor deve permanecer em série com o LED. Não ligar o LED diretamente entre D22 e GND. Com 5 V, 470 Ω limita a corrente a menos de 10,7 mA mesmo considerando a estimativa conservadora de queda nula no LED. Isso é uma conta de limite, não uma medição da montagem.

## Colocar o programa no Mega

1. Baixar esta pasta inteira. Manter `NEXUS_A01_Bancada.ino` e `controle_luz.h` juntos na pasta chamada **NEXUS_A01_Bancada**.
2. Abrir o arquivo `.ino` no Arduino IDE. A aba do arquivo `.h` deve aparecer junto. Não é necessário instalar biblioteca de sensor para este ensaio.
3. Selecionar a placa **Arduino Mega or Mega 2560**, processador **ATmega2560**, e a porta correspondente ao cabo USB. Se a porta não aparecer, registrar a mensagem e identificar o conversor USB da placa antes de instalar qualquer driver.
4. Usar **Verificar** e depois **Carregar**. Aguardar a conclusão indicada pelo IDE.
5. Abrir o Monitor Serial em **115200 baud**. É a janela em que digitaremos os comandos e veremos as leituras.

Ao abrir o Monitor Serial, a placa pode reiniciar. Nesse caso, o programa começa novamente desligado e perde a calibração anterior. Isso é previsto nesta versão.

## Fazer o teste, nesta ordem

### 1. LED, sem depender de sensor

Enviar `1` pelo Monitor Serial: o LED deve acender. Enviar `0`: deve apagar. Se não funcionar, conferir D22, resistor, polaridade do LED e GND com a alimentação retirada. Não passar ao automático antes de resolver essa etapa.

### 2. Leitura de movimento

O programa mostra `PIR=0` ou `PIR=1` a cada segundo. Aguardar a estabilização do sensor e observar o retorno a zero sem movimento. O automático fica bloqueado nos primeiros **60 segundos** do programa, como espera inicial de bancada; o módulo real pode exigir mais tempo de estabilização.

Passar a mão em frente ao sensor e observar a mudança. PIR detecta variações associadas a movimento; não garante detectar uma pessoa imóvel. A duração de `PIR=1` também depende do ajuste de tempo e do modo de retrigger do módulo. Não fixar posição final na casa antes desse ensaio.

### 3. Calibração da luminosidade

Com o sensor exposto à condição que vocês considerarão **clara**, esperar a leitura filtrada estabilizar e enviar `c`. Cobrir o sensor ou criar a condição **escura**, esperar estabilizar e enviar `e`.

O programa verifica se as leituras têm separação suficiente e identifica automaticamente se o valor aumenta ou diminui no escuro. Se aparecer `CALIBRACAO RECUSADA`, refazer o contraste. Não escolham um número aleatório para esconder o problema.

Os números são leituras brutas do conversor, na faixa 0 a 1023. **Não são lux.** Nesta revisão, exige-se diferença de pelo menos 80 unidades e usa-se margem de 20 unidades em torno do ponto central; são escolhas iniciais de ensaio, a ajustar se os testes indicarem necessidade.

### 4. Funcionamento automático

Depois da calibração aceita e da estabilização do PIR, enviar `a`.

- Claro + movimento: o LED fica apagado.
- Escuro + movimento: o LED acende.
- Escuro + saída do PIR voltando a zero: o LED permanece aceso por 5 segundos após a última leitura alta e depois apaga.
- Voltar à condição clara: o LED apaga quando a leitura filtrada atravessa a fronteira de claro.

Os 5 segundos são parâmetro de bancada. O tempo próprio do PIR pode se somar a eles. O filtro também introduz uma pequena demora na resposta à luz. Iluminar apenas o sensor LDR, sem mover a mão diante do PIR, ajuda a separar os efeitos.

Enviar `0` interrompe o automático. Enviar `1` liga manualmente, independentemente da luminosidade. Ao retornar com `a`, o sistema exige uma nova leitura alta do PIR; não reaproveita uma detecção já encerrada antes do retorno.

## Comandos

| Comando | Efeito |
| --- | --- |
| `1` | Liga o LED manualmente |
| `0` | Desliga o LED e sai do automático |
| `c` | Registra a leitura atual como condição clara |
| `e` | Registra a leitura atual como condição escura |
| `a` | Solicita modo automático; exige calibração e estabilização |
| `s` | Mostra o estado atual |
| `?` | Mostra a ajuda |

## O que registrar e trazer para a próxima revisão

Copiar as leituras `CLARO=`, `ESCURO=` e `CENTRO_ADC=`, anotar quanto tempo o PIR fica em 1, guardar uma foto das ligações e um vídeo curto mostrando entrada e resposta. Registrar as falhas, sem preencher resultado por suposição. A ficha está em [Registro_Teste_A01.csv](Registro_Teste_A01.csv).

Essa demonstração ainda não é o firmware completo da casa. Não detecta de maneira confiável desconexão dos sensores e não é um sistema de detecção de ocupação ou segurança certificado. A luz do próprio LED não deve incidir diretamente sobre o LDR; verificar possível realimentação antes de instalá-los na maquete.

## Verificação em computador

Os testes de decisão estão em [Testes_A01](../Testes_A01/). Verificam calibração nas duas polaridades, bloqueio inicial, histerese, permanência, troca de modos e transbordamento do contador de tempo. Eles não reproduzem o comportamento físico do PIR, a resposta óptica do LDR ou uma falha de ligação.

## Referências técnicas consultadas

- [Arduino Mega 2560, documentação da placa](https://docs.arduino.cc/hardware/mega-2560/).
- [Joy-IT, módulo KY-018](https://sensorkit.joy-it.net/en/sensors/ky-018).
- [Adafruit, leitura de PIR com Arduino](https://learn.adafruit.com/pir-passive-infrared-proximity-motion-sensor/using-a-pir-w-arduino).
- Pinagem e inventário do NEXUS R02. As referências de fabricantes orientam o estudo; a identificação da placa recebida continua necessária.
