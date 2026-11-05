# Validação do kit de módulos R02

Casa Inteligente | NEXUS | ExpoTech. 05/11/2026.

## Compilação para a placa

Os seis novos sketches foram compilados individualmente para **arduino:avr:mega:cpu=atmega2560**, com código de saída zero. Ferramentas: Arduino CLI 1.5.2-rc.1, plataforma arduino:avr 1.8.8 e avr-gcc 7.3.0-atmel3.6.1-arduino7.

| Sketch | Programa, bytes | Variáveis globais, bytes |
| --- | ---: | ---: |
| NEXUS_A02_Brise | 5792 | 365 |
| NEXUS_A03_RFID | 6864 | 237 |
| NEXUS_A04_Ambiente | 6310 | 225 |
| NEXUS_A05_Agua | 6804 | 261 |
| NEXUS_A08_Botoes | 3994 | 250 |
| NEXUS_A09_Entradas | 3208 | 197 |

O Mega deste alvo oferece 253.952 bytes para o programa e 8.192 bytes de SRAM. Esses números são do compilador, não medição de consumo elétrico nem garantia de espaço em uma versão integrada. O A01 anterior possui seu próprio registro em Testes_A01.

Bibliotecas utilizadas:

- Servo: 1.3.0.
- DHT sensor library: 1.4.7.
- Adafruit Unified Sensor: 1.1.15.
- MFRC522: 1.4.12.

Exemplo de compilação reproduzível a partir da raiz, com as bibliotecas instaladas:

```sh
arduino-cli compile --fqbn arduino:avr:mega:cpu=atmega2560 07_Codigo/NEXUS_A04_Ambiente
```

## Testes de software executados

| Parte | Evidência executada | Resultado |
| --- | --- | --- |
| Controle lógico de água | teste_agua.cpp, 26 verificações | Aprovado |
| Sequência da garagem | teste_portao.cjs, 16 cenários | Aprovado |
| Scripts da interface HTML | teste_interface.cjs, entrada, saída, obstáculo e falha | Aprovado em DOM mínimo; sem inspeção visual de navegador |
| Supervisor USB | 6 testes Python, incluindo CSV e servidor HTTP local | Aprovado; sem porta USB real |
| Cálculo solar | 4 testes Python, incluindo rejeição de premissas incompletas/inválidas | Aprovado |

Comandos para reprodução:

```sh
g++ -std=c++11 -Wall -Wextra -Werror -pedantic 07_Codigo/Testes_Modulos/teste_agua.cpp -o /tmp/nexus_agua_teste
/tmp/nexus_agua_teste
node 09_Simulacoes/Garagem/teste_portao.cjs
node 09_Simulacoes/Garagem/teste_interface.cjs
python -m unittest discover -s 07_Codigo/Supervisor_USB -p 'teste_*.py'
python -m unittest discover -s 06_Calculos/Solar -p 'teste_*.py'
```

O exemplo de saída `/tmp` é para Linux/macOS. No Windows com g++ instalado, escolher uma pasta gravável e um executável `.exe`. Não é necessário executar esses testes de desenvolvimento para seguir os guias no Arduino IDE.

## Limite da validação

Nenhuma placa foi conectada neste ambiente. Não houve upload físico, acionamento de servo, leitura real de DHT/RFID, calibração de nível/vazão ou ensaio de potência. Bomba e solenoide continuam sem acionamento nos sketches; a garagem continua simulada. Os programas não foram integrados em um único firmware.

Os registros CSV nas pastas dos módulos permanecem sem resultados físicos. Testes em computador não devem ser preenchidos nessas fichas como se fossem ensaios da montagem.

## Identificação dos fontes compilados

SHA-256 dos arquivos `.ino`/`.h` desta compilação:

- `07_Codigo/NEXUS_A02_Brise/NEXUS_A02_Brise.ino`: `a36c02ec0e9aa6415141badcda00957d4ad6fffebb35bd4ea454fdda7e18272a`.
- `07_Codigo/NEXUS_A03_RFID/NEXUS_A03_RFID.ino`: `5b8b37d0854c1c3247221228e59f762b230297db81566cf06a25693e36280eab`.
- `07_Codigo/NEXUS_A04_Ambiente/NEXUS_A04_Ambiente.ino`: `b45e86ea4b18b2100ac93f9c471f31d6b234c32ef9319598495261b070f6a825`.
- `07_Codigo/NEXUS_A05_Agua/NEXUS_A05_Agua.ino`: `b4c4c07aebbc828b36155b9b292976c47127af307b13ce03f6d29746bfc59da6`.
- `07_Codigo/NEXUS_A05_Agua/controle_agua.h`: `08eeca918ebd638d077709d655ec89901c47c5a5fd217970792a8efd1dc4bfbc`.
- `07_Codigo/NEXUS_A08_Botoes/NEXUS_A08_Botoes.ino`: `635fdc5f923b6fcc09f2e8cd9b9d7b5cc3897d5961289b5ca5f48ad1100590db`.
- `07_Codigo/NEXUS_A09_Entradas/NEXUS_A09_Entradas.ino`: `fcba16b755992a87de2c4684081124dda2c0f736c5f5caeb11ae65e18663977d`.
