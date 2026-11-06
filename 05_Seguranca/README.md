# Segurança e rede

**Nova entrega:** [Rede e segurança R01](Rede_R01/), com quatro pranchas, CAD, coordenadas, topologia e complementos por escopo. Inclui um [simulador offline de alarmes](Rede_R01/NEXUS_Simulador_Alarmes_R01.zip), com 18 cenários de lógica testados. A interface visual aguarda conferência manual.

O [inventário](../08_BOM/) relaciona PIR, RFID, solenoide e câmeras OV7670. A disponibilidade dos componentes não comprova captura de imagem, processamento ou alarme em funcionamento.

A R01 já relaciona acesso, intrusão, fumaça e vazamento, com posições propostas e matriz funcional. Ainda é necessário definir dispositivos, cobertura, interfaces, alimentação e resultados físicos. Identificar os dispositivos adicionais necessários. Botões que simularem eventos devem ser apresentados como simulação de entrada.

A R01 propõe central, quatro pontos de dados, AP e duas reservas residenciais de câmera IP, com sete enlaces em estrela. A comunicação Mega/ESP32, Wi-Fi/MQTT, dispositivos, banda, PoE e Smart Grid ainda dependem de implementação e dimensionamento. O [supervisor USB local](../07_Codigo/Supervisor_USB/README.md) já foi preparado e testado por software, mas não representa uma rede residencial ou comunicação ESP32 validada. Sua leitura de porta física ainda será ensaiada.

O comportamento do portão em obstáculo, falha e emergência está na [especificação de automações](../04_Automacao/NEXUS_Especificacao_Automacoes_R01.txt).
