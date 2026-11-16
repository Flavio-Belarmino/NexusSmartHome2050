# Validação de software R06

Execução em computador em 16/11/2026; alvo Arduino Mega 2560. O arquivo publicado foi copiado integralmente da revisão R06 usada no desenvolvimento, sem mudanças de comportamento para esta publicação documental.

## Compilação executada

- Arduino AVR Boards 1.8.6; alvo `arduino:avr:mega` / ATmega2560.
- Programa: **45.094 bytes (17%)** de 253.952 bytes disponíveis.
- Variáveis globais: **2.823 bytes (34%)**; 5.369 bytes de SRAM restantes, segundo a ferramenta.
- Compilação concluída sem erro. Isso não verifica alimentação, corrente dos atuadores ou resposta física.

Bibliotecas instaladas no ambiente da compilação:

| Biblioteca | Versão |
| --- | --- |
| MCUFRIEND_kbv | 3.0.0-Release |
| Adafruit GFX Library | 1.13.0 |
| Adafruit TouchScreen | 1.1.6 |
| Adafruit BusIO | 1.17.4 |
| MFRC522 | 1.4.12 |
| Servo | 1.3.0 |
| DHT sensor library | 1.4.7 |
| Adafruit Unified Sensor | 1.1.15 |

Comando reproduzível após instalar placa e bibliotecas:

```sh
arduino-cli compile --fqbn arduino:avr:mega 07_Codigo/NEXUS_TFT_Integrado_R06
```

## Testes de lógica executados

[Script Python/C++](tests/teste_logica_r06.py), com entradas simuladas e stubs das bibliotecas. Resultado: **PASS**. O script lê o próprio fonte publicado, compila as verificações com g++ e executa as asserções.

Cobertura: temporização do servo e recuperação de passos por tempo; manual/RFID e espera de 3 s; UIDs autorizados/negado; bloqueio da bomba por nível inclusive em manual; limiares e histerese de água/LDR; alarme térmico, apito intermitente, cancelamento e rearme; teste manual de 3 s sem interferir no alarme real; aviso global DHT e recuperação; calendário/relógio; navegação/touch; progresso visual lento do portão, água/onda, lua/sol e gradiente do termômetro.

As verificações de desenho exercitam as funções e seus estados, não substituem a observação do TFT físico. Compilação não prova estabilidade elétrica nem esforço/velocidade mecânica. Relatos de bancada e pendências físicas constam no [registro separado](../../09_Simulacoes/Validacao/Registro_Ensaios_R06.csv). O reinício do Mega ao soar o alarme ainda não foi resolvido por estes testes.

## Integridade do fonte

SHA-256 do arquivo `.ino` publicado:

```text
19e13e635e1e2ef69e6170c968cbded1bcec7962465d27a6beb373bdf7d6cc53
```
