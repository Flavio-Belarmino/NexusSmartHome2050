# A09 | Diagnóstico das quatro entradas reservadas ao touch

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026.

O inventário informa “TTP32” de quatro canais, sem identificação suficiente da placa/chip. Este programa já prepara a observação de **D36, D37, D38 e D39**, preservando a R02. Não escolhe uma biblioteca ou polaridade de toque por suposição e não comanda atuadores.

## Antes da ligação

Identificar modelo, alimentação, GND, saídas e seus níveis. Só ligar saídas que tenham tensão compatível com a entrada do Mega, com GND comum e alimentação confirmada da placa. Não concluir que um nível zero significa “sem toque” sem observar o módulo real.

O programa não ativa pull-ups internos: entradas desconectadas podem flutuar. Sua leitura não é um teste de presença do módulo nem uma detecção confiável de fio rompido.

## Procedimento

1. Fotografar frente/verso e marcação do chip. Conferir a documentação antes de alimentar.
2. Após confirmar as interfaces, ligar as saídas aos quatro pinos reservados. Manter apenas esse módulo no ensaio.
3. Carregar o sketch no Mega, abrir Monitor Serial em 115200 e enviar `i` para habilitar a leitura.
4. Registrar o vetor de quatro entradas sem tocar e ao tocar cada canal separadamente. Observar se a saída é momentânea ou retida e se o nível ativo é alto ou baixo.
5. Enviar `x` para suspender a leitura; os valores passam a `null`. Isso não corta a alimentação do módulo.

Esses resultados permitirão escrever a interpretação e os comandos do touch na revisão integrada. Não há teste físico deste módulo concluído.
