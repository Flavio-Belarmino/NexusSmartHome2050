# A03 | RFID: leitura e autorização no LED

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026. Sketch independente para Mega. A autorização acende o LED da própria placa por 3 segundos. **A solenoide não é acionada; D7 permanece como entrada.**

## Conferir antes da ligação
O RC522 é um dispositivo de lógica de 3,3 V. O Mega usa sinais de 5 V. Confirmar a placa e preparar interface de níveis apropriada antes de conectar seus sinais. Alimentar o módulo com 3,3 V compatível com a corrente necessária. Não ligar VCC do RC522 em 5 V. A biblioteca não corrige uma incompatibilidade elétrica.

| Função RC522 | Mega / interface |
| --- | --- |
| SDA / SS | D53, com adaptação de nível para o RC522 |
| SCK | D52, com adaptação de nível |
| MOSI | D51, com adaptação de nível |
| MISO | D50, retorno com nível compatível com a entrada do Mega |
| RST | D49, com adaptação de nível |
| VCC / GND | 3,3 V compatível / GND comum |

A conexão chamada SDA neste módulo funciona como seleção SPI neste ensaio. Não é a ligação I²C SDA do Mega. A solenoide, relé e respectivos drivers ficam desconectados.

## Programa e teste
Instalar **MFRC522**, de GithubCommunity/miguelbalboa, versão compilada 1.4.12. O SPI acompanha a plataforma Arduino. Selecionar Mega/ATmega2560 e Monitor Serial 115200.

1. O sketch inicia sem ativar o leitor. Após conferir a interface, enviar `i`. O programa mostra a versão respondida pelo chip. Resposta 0 ou 255 bloqueia o leitor.
2. Apresentar um cartão antes de cadastrar: não deve autorizar.
3. Enviar `g` e apresentar voluntariamente o cartão escolhido. Isso cadastra **um cartão** apenas na RAM e não libera acesso nessa leitura.
4. Retirar o cartão do campo, aguardar e reapresentá-lo: o LED da placa deve acender por 3 segundos.
5. Retirar e apresentar outro cartão: deve negar e manter o LED apagado.
6. Enviar `c` para apagar o cadastro. Reiniciar a placa também o apaga.

O programa compara UID para uma demonstração acadêmica. Isso não é autenticação criptográfica resistente a clonagem e não deve proteger uma porta real. Não publicar identificadores de cartões reais ou credenciais em arquivos do projeto.

## Para avançar à fechadura
Ainda identificar a corrente da solenoide de 6 V, fonte adequada, driver, proteção indutiva, lógica de liberação e corte de energia. A aprovação do cartão no LED não comprova que a porta está aberta ou que a fechadura funciona.

Referências: [biblioteca MFRC522](https://github.com/miguelbalboa/rfid); [datasheet NXP](https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf); pinagem NEXUS R02. Ensaio físico pendente.
