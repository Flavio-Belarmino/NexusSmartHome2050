# Identificação e complementos por função

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026. Base: inventário recebido e pinagem R02. Esta lista orienta a conferência; não é orçamento nem compra final.

| Item/função | Conferir no material recebido | Complemento ou decisão necessária |
| --- | --- | --- |
| Mega e ESP32 | Modelo das placas, conversor USB, alimentação e pinos disponíveis | Interface de comunicação de 5 V/3,3 V e mapa do ESP32 antes de interligar |
| RFID RC522 | Placa, pinos, regulador e corrente | Adaptação de níveis adequada a SPI; não escolher conversor apenas por aparência ou por ser anunciado para I²C |
| Servo do brise | Modelo, alimentação e corrente em movimento/travamento admissível | Fonte DC compatível, ligações e mecanismo livre; servo continua reservado ao brise |
| Solenoide | Etiqueta de 6 V, corrente, tempo de uso e comportamento sem energia | Fonte/regulação, driver, proteção indutiva e definição física de liberação |
| Bomba RS-385 | Alimentação de 12 V, regime, partida e conexão hidráulica | Driver, proteção indutiva, proteção elétrica, bandeja e circuito de recirculação |
| Sensor de vazão | Modelo, alimentação, tipo/tensão da saída e fator | Interface para D2 e calibração em pulsos/litro antes de exibir L/min |
| HC-SR04 | Identificação e eco no recipiente | Posição e calibração; não retirar do reservatório para usar na garagem |
| Fita LED | Tensão, tipo, trecho e corrente | Driver e alimentação dimensionados depois da identificação |
| Relé | Número de canais, bobina, lógica ativa e interface | Uso só depois de confirmar entradas e cargas; o rótulo 10 A não define sozinho a aplicação |
| Touch “TTP32” | Fotografar placa/chip, quantidade de saídas e alimentação | Confirmar se a referência é TTP224 ou outro modelo antes de definir biblioteca e níveis |
| OV7670 | Módulo, presença de FIFO, pinagem, relógio e alimentação | Definir arquitetura de captura; duas câmeras disponíveis não equivalem a CFTV já funcionando |
| Garagem | Carrinho, mecanismo, massa, curso e vão | Atuador próprio, detecções externa/interna/vão, confirmação de posição e driver |
| Solar | Modelos de painel, controlador e bateria, química e Ah | Compatibilidade de carga/descarga, proteções e instrumentos; manter separado da alimentação principal |
| Instalação | Cabos, bornes, conectores, fixação e isolamento | Quantificar por percurso e permitir inspeção/manutenção |

Não foi identificado no inventário um conjunto completo e especificado para detecção física de fumaça/incêndio e vazamento. Essas funções precisam de definição própria. Um botão de simulação não deve ser apresentado como sensor físico do evento.

## Fotografias que resolvem pendências

Quando o material estiver reunido, registrar frente/verso e etiqueta de: fontes, controlador solar, bateria, relé, fita, touch, sensor de vazão, ESP32, câmeras e botão de emergência. O objetivo é fechar modelos e interfaces; não é necessário aguardar essas fotos para executar a simulação da garagem ou estudar o código.
