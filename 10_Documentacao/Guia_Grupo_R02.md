# Guia do grupo R02

NEXUS | 06/11/2026 | Preparação para bancada, montagem e explicação do projeto.

## O que estamos construindo

O NEXUS reúne o estudo de uma residência para quatro pessoas e uma maquete para demonstrar funções escolhidas de automação. O projeto residencial tem instalações dimensionadas por hipóteses documentadas. A maquete usa componentes próprios de baixa tensão e precisa de ensaios físicos. O que aparece desenhado não deve ser apresentado como instalado ou testado sem evidência.

## Primeiro encontro com os materiais

1. Abrir a [lista consolidada](../08_BOM/Consolidacao_R02/) e conferir componentes/etiquetas. Fotografar as peças que ainda estão genéricas. Separar o servo do brise e o HC-SR04 do reservatório.
2. Conferir as peças civis e montar a distribuição a seco. Medir carrinho, vão e curso da garagem. Definir onde ficarão placas, mangueiras, tampas e conectores acessíveis.
3. Começar pelo [A01 de iluminação](../07_Codigo/NEXUS_A01_Bancada/README.md). Separar só o material desse ensaio e seguir o guia por etapas: LED, leitura, calibração e automático.
4. Preencher a ficha do módulo com resposta observada e fotos. Se falhar, registrar a falha antes de passar ao próximo teste. O nome de quem executou e a data devem ser reais.
5. Continuar pela [ordem dos módulos](Guia_Bancada_Modulos.md). Cada sketch substitui o anterior no Mega. Bomba e fechadura dependem das interfaces ainda pendentes; os programas atuais não as acionam.
6. Antes de colar ou fechar, revisar a [matriz de compatibilização](Compatibilizacao_R02.md), testar conexões e demonstrar manutenção/acesso às peças.

## O que cada integrante precisa conseguir explicar

| Tema | Explicação essencial | Onde estudar | Limite que precisa conhecer |
| --- | --- | --- | --- |
| Arquitetura | Ambientes, dimensões, representação e circulação | Arquitetura R02 e memorial | Garagem e sistema construtivo residencial ainda pendentes |
| Elétrica | Como as cargas formam circuitos e como o quadro os organiza | Caderno elétrico R02 | Potências/fornecimento são cenário de estudo; não são ligações da maquete |
| Hidráulica | Caminho da água fria/quente, esgoto, ventilação e chuva | Caderno hidráulico R02 | Diâmetros/cotas dependem das hipóteses; não houve medição de campo |
| Iluminação | Relação entre presença, claro/escuro e permanência | A01 | Calibração e resposta física precisam ser testadas |
| Brise | Comando de posição e limites de movimento | A02 | Falta verificar o mecanismo montado |
| Acesso | Leitura do cartão, autorização e recusa | A03 | LED de autorização não prova destravamento físico |
| Ambiente/água | Leitura, falha de sensor e registro de valores | A04/A05 | Vazão requer calibração; bomba sem acionamento no sketch atual |
| Garagem | Abrir, confirmar posição/passagem, aguardar vão livre e fechar | Simulador e especificação R01 | Sequência virtual não comprova mecanismo real |
| Rede/segurança | Central, comunicação proposta e origem dos alarmes | Rede R01 | Captura de vídeo e rede física não comprovadas |
| Materiais/ESG | Reserva dos componentes e razão de cada escolha | BOM e memorial R02 | Potencial de economia não é economia medida |

## Exercício para explicar sem decorar

Cada integrante escolhe uma função e explica: qual entrada o sistema recebe, o que decide, qual saída comanda, como reage a uma falha e qual teste comprova o resultado. Depois, outro integrante repete a explicação e troca de função. O objetivo é que todos compreendam o conjunto; a equipe pode dividir tarefas sem restringir o conhecimento a uma única pessoa.

Exemplo A01: “O programa lê presença e luminosidade. No automático, acende quando há presença e está escuro; usa um tempo de permanência. O teste precisa mostrar claro, escuro, presença e ausência. Por enquanto temos programa compilado e teste de lógica; o registro de bancada vai mostrar a resposta dos nossos sensores.” Atualizar a última frase quando houver evidência física.

## Como mostrar o avanço com honestidade

| Estado | O que permite afirmar |
| --- | --- |
| Proposto/desenhado | Há uma solução documentada, ainda sem confirmação de execução |
| Calculado | O resultado foi obtido nas hipóteses indicadas |
| Compilado | O código foi aceito pela ferramenta para a placa definida |
| Testado por software | Cenários lógicos foram executados; não demonstra sensor/mecânica |
| Testado em bancada | Há um ensaio físico identificado e registrado |
| Integrado e demonstrado | O conjunto funciona com configuração/versão e evidências registradas |

Consultar os arquivos e resultados efetivos antes de preencher vídeo, slides ou falas. Não atribuir uma função aos integrantes por suposição. O [controle de entregas](Controle_de_Entregas.md) mantém as demais etapas e pendências do trabalho.
