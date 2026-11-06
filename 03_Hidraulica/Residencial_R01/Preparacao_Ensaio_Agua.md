# Preparação do ensaio de água

Casa Inteligente | NEXUS | ExpoTech. Preparação antes da montagem. Não há resultados físicos registrados aqui.

## Agora, sem água nem bomba

1. Separar Mega, HC-SR04, jumpers e cabo USB. Conferir a leitura e a calibração conforme o [A05](../../07_Codigo/NEXUS_A05_Agua/README.md).
2. Fotografar as marcações da bomba RS-385 e do sensor Hall de vazão, incluindo fios/conectores. O inventário não confirma a saída elétrica nem pulsos por litro do sensor.
3. Medir os diâmetros externos dos bocais com régua/paquímetro, altura/largura dos recipientes e espaço disponível. Não comprar a mangueira somente pelo nome da bomba.

## Separar para a futura circulação em bandeja

| Item | O que conferir antes de comprar/montar |
| --- | --- |
| Recipiente e bandeja | Estanqueidade, acesso para limpar, estabilidade e contenção; dimensões reais |
| Bomba RS-385 | Variante, tensão, corrente, regime, posição de montagem, priming e aptidão para trabalhar com a água usada |
| Sensor de vazão | Modelo, faixa de vazão, direção, saída/tensão, conexões e fator de calibração |
| Mangueira/conexões | Compatibilidade com bocais, pressão, vedação e fixação; comprimento após medir percurso |
| Driver e proteção | Compatíveis com corrente nominal/partida e lógica da placa; proteção da carga indutiva e elétrica a detalhar |
| Alimentação | Fonte 12 V identificada; ligação e fusível/proteção dimensionados antes do ensaio |
| Suporte do HC-SR04 | Posição seca e estável; distância útil no recipiente; acesso e proteção contra respingos |
| Registro manual/retorno | Poder interromper e ajustar circulação sem depender apenas do programa |

Não energizar bomba com ligações ainda indefinidas. A documentação atual do A05 mantém o acionamento bloqueado. Antes do ensaio molhado, desenvolver e verificar o circuito de potência e a alimentação; não ligar a bomba diretamente ao pino do Mega.

## Evidências para registrar depois

Usar a ficha de ensaio do A05: versão do código, componentes identificados, leituras com referência de régua/recipiente graduado, falhas, tempos e fotos da montagem. Guardar também o resultado que falhou. Não declarar litros/minuto sem calibrar nem porcentagem de volume a partir de altura sem conhecer o formato do recipiente.

A bancada é uma demonstração em circuito fechado. Não interligar à água da residência, não consumir a água do ensaio e manter a eletrônica fora da área molhada. O ensaio não valida água potável, tratamento de chuva ou instalação hidráulica residencial.
