# Stack e tecnologias

Atualização de 16/11/2026. A tecnologia listada pertence ao firmware, aos documentos ou aos estudos identificados abaixo.

| Tecnologia | Uso nesta entrega |
| --- | --- |
| Arduino Mega 2560 / Arduino C++ | Firmware integrado R06 de controle local |
| MCUFRIEND_kbv, Adafruit GFX e Adafruit TouchScreen | TFT ILI9341 paralelo e touch resistivo calibrado |
| Servo e MFRC522 | MG996R do portão e leitura RC522 |
| DHT sensor library / Adafruit Unified Sensor | Temperatura/umidade; alarme e indicação de falha |
| Python | Geração de desenhos, cálculos, ferramentas auxiliares e testes de software |
| HTML/CSS/JavaScript | Simuladores de garagem/alarmes e interface do supervisor USB, como estudos separados |
| DXF, CSV, JSON e PDF | Desenhos editáveis, pinagem, dados e documentação |
| GitHub / Git | Publicação e histórico de revisões |
| ESP32 / Wi-Fi | Previsto na arquitetura, sem integração à montagem R06 |

## Texto para o campo Stack/tecnologias

Arduino Mega 2560 (C++), TFT ILI9341 com touch resistivo, Servo/MG996R, RFID RC522/MFRC522, DHT22, LDR, sensores de água e nível, relé e bomba. Bibliotecas MCUFRIEND_kbv, Adafruit GFX, TouchScreen, Servo e DHT. Python e HTML/CSS/JavaScript nos cálculos, testes e simuladores; CAD/DXF, CSV/JSON, PDF e GitHub na documentação. ESP32/Wi-Fi previsto, ainda não integrado.

A lista não declara sensores de fumaça, câmeras, comunicação sem fio ou geração elétrica funcionando na maquete. A validação física final e a investigação do reinício do Mega continuam abertas.
