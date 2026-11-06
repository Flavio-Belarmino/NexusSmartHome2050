# Rede e segurança R01

Casa Inteligente | NEXUS | ExpoTech. Estudo de 05/11/2026 sobre a geometria R02, sem alterar paredes/aberturas. Esta revisão reúne o layout de dados/segurança, a topologia e um protótipo computacional da lógica de alarmes. Não conclui a instalação física ou o projeto executivo.

| Arquivo | Conteúdo |
| --- | --- |
| [PDF de quatro pranchas](NEXUS_Rede_Seguranca_R01.pdf) | Rede de dados; segurança; topologia/interfaces; matriz funcional e ensaios |
| [Rede em DXF](RS01_Rede_Dados.dxf) | Pontos, central e sete percursos em estrela |
| [Segurança em DXF](RS02_Seguranca.dxf) | Posições de referência de câmeras, acesso e detecção |
| [Coordenadas](Pontos_Rede_Seguranca_mm.csv) | 16 referências em mm da residência e da maquete, com alturas propostas |
| [Enlaces](Cabos_Dados_Estimativa.csv) | Vértices e estimativa geométrica de cada cabo |
| [Complementos por escopo](Complementos_por_Escopo.csv) | Conferências e itens da maquete separados dos equipamentos da residência |
| [Modelo](Modelo_Rede_Seguranca_R01.json) | Dados e premissas do estudo |
| [Contrato futuro](Contrato_Telemetria_Proposto.json) | Campos e condições para desenvolver a comunicação; não é protocolo implementado |
| [Simulador](Simulador_Alarmes.html) | HTML offline, acompanhado de Controle_Alarmes.js |
| [Pacote do simulador](NEXUS_Simulador_Alarmes_R01.zip) | Extrair e abrir o HTML, com o JS na mesma pasta |
| [Lógica](Controle_Alarmes.js) e [testes](Testar_Alarmes.cjs) | Máquina de estados virtual e cenários de software |
| [Gerador](Gerar_Rede.py) | Fonte do PDF/CAD/tabelas |
| [Verificação](Verificacao_R01.md) | Testes, auditoria CAD e limites |

## Rede da residência

CT01 propõe uma central no apoio AM09. Quatro pontos de dados, um ponto de acesso e duas câmeras residenciais IP somam sete enlaces em estrela. Há uma proposta de entrada de fibra até ONT/roteador, ainda sem definir lote, operadora, conector ou trajeto externo. As posições TD indicam uso pretendido; caixas e instalação em parede/mobiliário precisam de compatibilização.

Os sete destinos e o uplink para o roteador ocupam oito portas do switch proposto. Duas portas adicionais de reserva levam à necessidade de capacidade igual ou superior a dez portas. Modelo, banda, PoE, alimentação, armazenamento de vídeo e proteção precisam ser dimensionados. Não é uma especificação de compra de equipamento para a maquete.

O comprimento geométrico dos enlaces é **71,450 m**: projeção do trajeto mais subidas/descidas até um plano proposto de 2.600 mm, sem folgas, patchcords ou reservas. Essa estimativa é por cabo individual, sem emendas nos cruzamentos. **Não é lista de corte nem quantitativo liberado para compra.** Verificar alturas, estrutura, percursos, separação das instalações, caixas, terminações e ensaios de cabeamento.

AP01 é uma posição inicial. Não há estudo de propagação nem garantia de cobertura/capacidade Wi-Fi. As câmeras têm apenas direção indicativa, sem campo de visão, alcance, resolução útil, reconhecimento ou privacidade de enquadramento verificados.

## Central e comunicação da maquete

CT01 representa a central da residência. Na maquete, a eletrônica continua na central externa prevista na implantação R02. Não se deve tentar acomodar equipamentos reais por simples redução de escala; conferir placas, conectores, fixações, ventilação e acesso.

Para comunicação futura, a R02 já reserva **D18 TX1 / D19 RX1** no Mega. É necessária uma interface elétrica compatível com os dois dispositivos; o ESP32 ainda precisa de modelo/GPIOs identificados. Não conectar o TX de 5 V diretamente ao ESP32. Não há novo circuito de adaptação ou atribuição de GPIO nesta revisão.

Wi-Fi e MQTT autenticado, com TLS configurado, são propostas para telemetria local. A primeira etapa deverá ser somente leitura, sem tópico de comando de atuadores. Enquadramento serial, limites de mensagem, erro, sessão/sequência, reconexão, credenciais, certificados e permissões ainda serão implementados e ensaiados. O JSON de contrato é uma especificação de desenvolvimento, não comprovação de tráfego real.

O [supervisor USB](../../07_Codigo/Supervisor_USB/) permanece disponível para um módulo de bancada por vez. Os testes anteriores foram de software; não demonstram UART Mega/ESP32, Wi-Fi ou rede doméstica funcionando. O novo simulador não se conecta ao supervisor nem ao broker.

Smart Grid permanece como interface futura do projeto elétrico. Não há integração com a concessionária ou medição de energia operacional. O experimento solar da maquete continua separado.

## Segurança e materiais

AC01 e PR01 preservam as coordenadas da R02. O PIR é **o mesmo dispositivo compartilhado com a iluminação**, e não dois sensores disponíveis. O RFID mantém o ensaio A03 por UID e LED: isso não é autenticação resistente a clonagem nem liberação física da solenoide.

RD01/RD02 propõem contatos das portas principal/lateral. SM01 é uma referência acadêmica de detecção de fumaça. VA01/VA02 propõem detecção de água junto à pia/lavadora. AL01 é sinalização demonstrativa. Os novos dispositivos e suas interfaces ainda não foram identificados ou atribuídos a pinos. A localização de SM01 não dimensiona cobertura de incêndio e não autoriza uso como alarme de proteção de pessoas.

As duas OV7670 do inventário são módulos de sensor de imagem, com captura, memória, relógio e controle a identificar. Não foram conectadas a Ethernet/PoE, não geram fluxo IP nesta revisão e não equivalem às câmeras residenciais propostas. Nenhuma imagem foi capturada ou reconhecida. Confirmar os módulos antes de escolher a arquitetura de vídeo.

O HC-SR04 continua reservado ao reservatório e o servo ao brise. Garagem terá mecanismo/detecções próprios. O mapa de entradas novas só será fechado após identificar hardware e revisar recursos da placa.

## O que vocês podem experimentar agora

Baixar o ZIP, extrair os arquivos e abrir `Simulador_Alarmes.html` em um navegador. Não é necessário internet, placa, cadastro ou instalação. O arquivo JS precisa permanecer ao lado do HTML. A página do arquivo no GitHub mostra o código; ela não executa o simulador.

1. Deixar tudo normal, armar a intrusão e marcar RD01. Deve aparecer uma ocorrência de intrusão.
2. Desarmar: a ocorrência continua retida. Desmarcar RD01 e clicar em limpar. A ocorrência deve sair.
3. Desarmado, marcar SM01: fumaça gera ocorrência independentemente do modo de intrusão.
4. Silenciar o indicador e marcar VA01: a nova causa reativa a indicação visual. Não existe som real.
5. Normalizar entradas e limpar. Pausar amostras; após mais de 3 segundos, deve aparecer SEM DADOS. Armar/limpar ficam bloqueados até dados atuais e entradas normais.
6. Baixar o registro JSON. Ele declara SIMULACAO e ausência de hardware; não renomear a origem como medição física.

A lógica retém ocorrências e distingue dado ausente de normalidade. O limite de 3 segundos e as regras de rearme são parâmetros de demonstração, não requisitos normativos de sistema de incêndio. O botão “desarmar” afeta apenas intrusão; não inibe as entradas virtuais de fumaça e água. Causas retidas não são apagadas por perda de dados. Reiniciar o simulador perde o histórico e volta ao estado inicial, sem persistência de alarmes de uso real.

A simulação não é um sistema de segurança certificado e não controla sirene, bomba, válvula, fechadura ou portão. Não captura câmeras e não autentica usuários. O funcionamento físico, sensores, sinalização, infraestrutura e instalação ainda precisam de projeto/ensaio.

## Verificação e reprodução

```sh
node 05_Seguranca/Rede_R01/Testar_Alarmes.cjs
python 05_Seguranca/Rede_R01/Gerar_Rede.py
```

Os testes verificam a lógica de 18 cenários em Node.js. A interface HTML recebeu conferência de estrutura e sintaxe; **não foi testada visualmente em navegador nesta entrega**, pois o navegador de teste bloqueou a abertura de arquivo local. Os passos acima orientam a conferência manual pela equipe. Não houve ensaio de hardware.

O gerador exige Python 3, `reportlab`, `ezdxf`, DejaVu Sans e o código publicado de hidráulica R01 para reutilizar a base gráfica. Não altera os dados arquitetônicos nem os arquivos da hidráulica. A escala arquitetônica/maquete é 20, em mm; as alturas e posições novas são propostas. O gerador confere ambientes, coordenadas preservadas e enlaces antes de escrever o PDF.

## Referências técnicas consultadas

- [Arduino Mega 2560 Rev3, Input and Output / Communication](https://store.arduino.cc/products/arduino-mega-2560-rev3): pinagem Serial1 e lógica de 5 V.
- [Espressif ESP-FAQ, Hardware related, tolerância dos GPIOs](https://docs.espressif.com/projects/esp-faq/en/latest/esp-faq-en-master.pdf): necessidade de compatibilizar os níveis elétricos.
- [Espressif GPIO & RTC GPIO, ESP32](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html): restrições dos pinos e necessidade de identificar a placa.
- [Espressif ESP-MQTT](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/mqtt.html): referência para implementação futura de mensageria e TLS, sem declaração de implementação no NEXUS.
- [OMNIVISION, apresentação técnica do OV7670](https://www.ovt.com/press-releases/omnivision-launches-seventh-generation-vga-camerachip-for-mobile-applications/): sensor VGA e interface de controle SCCB.
- [Roteiro BLUEPRINT](../../10_Documentacao/Regulamento/Roteiro_BLUEPRINT_2026_2.pdf): escopo de automação/cabeamento e segurança. Normas e critérios de projeto ainda devem ser consultados para dimensionamento e conformidade de cada sistema.

Consulta em 05/11/2026. As fontes fundamentam as interfaces descritas; não certificam o conjunto proposto.
