# Roteiro de bancada | 20/11/2026

## 1. Display primeiro

- Salvar o código anterior e conferir Mega selecionado no Arduino IDE.
- Desligar tudo e retirar os periféricos e fontes externas.
- Conferir alinhamento dos conectores e encaixar o shield sem deslocar uma posição.
- Usar somente USB no Mega. Instalar MCUFRIEND_kbv, Adafruit GFX Library e Adafruit TouchScreen, com as dependências solicitadas.
- Abrir os três arquivos do [ensaio isolado](../../07_Codigo/NEXUS_Display_Demo/README.md) na mesma pasta e gravar.
- Abrir Serial a 115200, registrar ID/diagnóstico e calibrar os quatro alvos.
- Conferir texto legível, orientação, cores sólidas e todos os botões, inclusive nos cantos.
- Deixar executar a demonstração por alguns minutos e observar reinícios ou falhas.

Critério: imagem estável, controles coerentes após calibração e resultado registrado. Se houver tela branca ou barras, registrar ID, foto e mensagens; não forçar um ID aleatório nem concluir dano apenas pelo sintoma.

## 2. Alimentação e componentes separados

Com o ensaio do display encerrado, desligar antes de mudar ligações. Verificar fontes e barramentos conforme a [proposta de distribuição](../../02_Eletrica/Distribuicao_DC_Proposta_2026-11-19.md).

| Ordem | Teste | Resultado a registrar |
| --- | --- | --- |
| 1 | AHT25 sozinho e depois DS3231 | Identificação, leitura coerente, horário e retenção quando houver bateria compatível |
| 2 | Um leitor RC522 com cartão do próprio kit | Leitura repetível; registrar resultado sem publicar UID autorizado |
| 3 | Um servo por vez, inicialmente sem mecanismo | Modelo, curso/comportamento e tensão durante movimento |
| 4 | Botões e um sensor IR de cada vez | Estado de repouso, acionamento e repetição |
| 5 | LEDs com resistores e semáforos | Pinagem e cores corretas, sem sobrecarga das saídas |
| 6 | Barra WS2812 | Cor, sequência e estabilidade da alimentação |
| 7 | Fita RGB e controlador | Pinagem e tensão reais; separar o teste da lógica do Mega |
| 8 | Circuito de água da montagem anterior | Sensor, relé e estado seguro da bomba; não acionar a seco |

A ordem pode ser interrompida após qualquer etapa aprovada. Priorizar funções estáveis para a apresentação, sem exigir integrar todos os complementos no mesmo encontro.

## 3. Integração gradual

Integrar primeiro leitura de um sensor ao display; depois botão; depois um atuador. Repetir o teste com cargas simultâneas previstas, observando tensão e reinícios. O programa demonstrativo continua sendo referência visual até receber leituras e comandos reais no firmware integrado.

## 4. Encerramento

Preencher a [ficha CSV](Registro_Nova_Montagem_2026-11-20.csv), guardar o firmware gravado e fotos das conexões. Em caso de erro de compilação, copiar a mensagem completa, nome do arquivo, placa e versões das bibliotecas. Em caso de falha física, anotar quais cargas estavam ligadas e o que aconteceu imediatamente antes.
