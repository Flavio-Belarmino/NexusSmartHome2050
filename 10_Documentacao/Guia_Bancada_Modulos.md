# Guia dos módulos: do código à bancada

Casa Inteligente | NEXUS | ExpoTech. R02 do kit de ensaios, 05/11/2026.

O material agora permite preparar vários sistemas antes de montar a casa. Cada pasta contém um programa de teste, suas ligações por função, comandos e ficha de resultados. A sequência abaixo evita começar pelas cargas que dependem de mais identificação elétrica.

**Os sketches são independentes. No único Mega do inventário, carregar outro programa substitui o anterior. Não copiar todos os `.ino` para uma mesma pasta.** A integração será outra revisão, depois dos testes de cada módulo. O supervisor USB também recebe um módulo por vez nesta etapa.

## O que já está preparado

| Ordem sugerida | Entrega | O que faz | O que depende da bancada |
| --- | --- | --- | --- |
| 1 | [A01 iluminação](../07_Codigo/NEXUS_A01_Bancada/README.md) | LED manual e automático por PIR/LDR | Identificação, calibração e resposta dos sensores |
| 2 | [A04 ambiente](../07_Codigo/NEXUS_A04_Ambiente/README.md) | Temperatura/umidade e indicação de erro | Ligações, leituras e comparação com referência |
| 3 | [A08 botões/LEDs](../07_Codigo/NEXUS_A08_Botoes/README.md) | Onze LEDs, quatro botões e parada lógica retida | Identificação dos contatos e resposta de cada canal |
| 4 | [A02 brise](../07_Codigo/NEXUS_A02_Brise/README.md) | Comandos do servo e resposta à luminosidade | Fonte DC, curso livre e depois mecanismo |
| 5 | [A03 RFID](../07_Codigo/NEXUS_A03_RFID/README.md) | Cadastro temporário e autorização no LED | Interface 3,3/5 V e leitura de cartões |
| 6 | [A05 água](../07_Codigo/NEXUS_A05_Agua/README.md) | Distância/nível e permissão lógica de bomba | Eco no recipiente, modelo/fator do sensor de vazão |
| Identificação | [A09 entradas/touch](../07_Codigo/NEXUS_A09_Entradas/README.md) | Leitura bruta de quatro canais reservados | Modelo, alimentação, níveis e comportamento do módulo |
| Pode fazer agora | [A07 garagem](../09_Simulacoes/Garagem/README.md) | Simulação funcional com entrada, saída, obstáculo e falhas | Carrinho, geometria, atuação e sensores reais |
| Opcional | [Supervisor USB](../07_Codigo/Supervisor_USB/README.md) | Painel local e registro de telemetria | Porta USB e execução no computador |
| Estudo | [A06 solar](../06_Calculos/Solar/README.md) | Cálculo de energia com premissas explícitas | Modelos, compatibilidade elétrica e medições |

## Preparar o computador

Usar o Arduino IDE instalado a partir do fornecedor oficial. Os exemplos são para **Arduino Mega or Mega 2560 / ATmega2560**. Ligar por USB, selecionar a porta identificada pelo IDE e usar primeiro Verificar, depois Carregar. O Monitor Serial de todos os módulos está em **115200 baud**.

Cada `.ino` deve estar em uma pasta com o mesmo nome. Manter os `.h` da pasta junto dele. As bibliotecas necessárias estão indicadas nos guias: A02 usa Servo; A03 usa MFRC522; A04 usa DHT sensor library e Adafruit Unified Sensor. A01, A05 e A08 não precisam de bibliotecas externas de sensor.

O pacote ZIP do kit reúne as pastas. Extrair antes de abrir. Se surgir um erro, copiar a mensagem completa, informar a placa/porta selecionada e o módulo. Não editar vários pinos ou bibliotecas por tentativa sem registrar o que foi alterado.

## Preparar cada ensaio

1. Ler o guia apenas do módulo escolhido e separar os itens listados.
2. Identificar VCC, GND e sinal pelas marcações/datasheet, sem supor ordem física dos pinos pelas tabelas.
3. Conferir a alimentação prevista e fazer ligações com as fontes retiradas.
4. Carregar o programa e testar primeiro os comandos simples, depois o automático.
5. Registrar resultado observado, inclusive falhas, na ficha CSV. Guardar foto das ligações e vídeo de estímulo/resposta.

A03 indica acesso no LED e deixa D7 sem acionamento. A05 indica permissão lógica e deixa D8 sem acionamento. Não ligar a solenoide ou a bomba a esses pinos. Os drivers, proteções e fontes dessas cargas serão conferidos antes de liberar uma revisão de acionamento físico.

## O que não precisa esperar a montagem

O simulador da garagem abre como arquivo HTML no navegador, sem instalação. O supervisor pode ser experimentado em modo de demonstração, explicitamente identificado, antes de conectar a placa. O cálculo solar aceita hipóteses de estudo sem atribuí-las ao circuito real.

As dimensões do carrinho são necessárias para dimensionar a garagem e seu mecanismo. Elas não impedem os ensaios de iluminação, ambiente, botões ou a simulação da sequência do portão.

## Depois dos ensaios

Consolidar resultados e identificação dos módulos, completar as interfaces, integrar o firmware com tarefas não bloqueantes e registrar as interações entre sistemas. Só então fixar definitivamente sensores e cabos na maquete. Os projetos prediais elétrico/hidráulico, a garagem nas plantas e as soluções civis/ESG continuam como entregas próprias; este kit não os substitui.
