# NEXUS | Ensaio isolado do display 3,5 polegadas

Revisão de 19/11/2026. Este programa é separado da R06. Não controla os atuadores da maquete.

## Abrir e gravar

Abra [NEXUS_Display_Demo/NEXUS_Display_Demo.ino](NEXUS_Display_Demo/NEXUS_Display_Demo.ino) mantendo os três arquivos na mesma pasta. No Arduino IDE, selecione Arduino Mega or Mega 2560 / ATmega2560 e a porta do Mega.

Bibliotecas: MCUFRIEND_kbv, Adafruit GFX Library e Adafruit TouchScreen; aceitar dependências, incluindo Adafruit BusIO.

O alvo é um shield paralelo de 8 bits, 480 × 320, com touch resistivo. O ILI9486 é a identificação do anúncio; o controlador entregue ainda precisa ser lido e confirmado.

## Primeiro teste

- Guardar o código integrado anterior.
- Encaixar o shield com o Mega desligado, conferindo alinhamento e nomes dos pinos.
- Testar somente Mega + display pelo USB, sem demais fontes e periféricos.
- Carregar o programa e tocar os quatro alvos com a caneta, soltando entre pontos.
- Abrir o Monitor Serial em 115200 para conferir ID e diagnóstico.

A calibração válida fica na EEPROM. Sem toque por 30 segundos, inicia a troca automática para permitir avaliar a imagem. A descoberta dos pares tenta o método do exemplo diagnose_Touchpins; não há garantia de detectar todos os lotes.

## Comandos pelo Serial

0 início; 1 portão; 2 luzes; 3 clima; 4 energia; 5 água; 6 acesso; 7 alertas; 8 testes. A liga/pausa a troca automática; C recalibra; T abre teste de cores.

## Telas e limites

Oito páginas de navegação, mais diagnóstico e cores. Ícones e animações desenhados pelo código, sem cartão SD. Todos os dados são ilustrativos e todos os comandos são virtuais. O teste não comprova carregamento solar, vazão, posição do portão ou leitura real de sensores.

## Verificação já executada

Compilação real para arduino:avr:mega: aprovada, com 38.950 bytes de programa e 603 bytes globais na versão entregue em 18/11. Bibliotecas utilizadas: MCUFRIEND_kbv 3.0.0-Release, Adafruit GFX 1.13.0, Adafruit TouchScreen 1.1.6 e BusIO 1.17.4; core AVR 1.8.6.

Foram verificados em computador: transformação de calibração com troca/inversão de eixos, rejeição de dados inconsistentes, alvos do menu, controles virtuais, sequência automática e tempo limite. As telas foram renderizadas com os desenhos da GFX. Ainda não há ensaio físico do display recebido.
