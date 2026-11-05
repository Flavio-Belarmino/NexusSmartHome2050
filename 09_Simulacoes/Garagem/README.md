# A07 | Simulador funcional da garagem

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026.

Baixar **NEXUS_Garagem_Simulador.html**, salvar e abrir no navegador. Ele contém a lógica e a interface, funciona sem internet e não se conecta a nenhum equipamento. No GitHub, usar o botão de download do arquivo; a visualização do código HTML não executa o simulador.

## O que já pode ser experimentado
Entrada e saída automáticas, aproximações externa/interna, passagem pelo vão, confirmação de posição, fechamento após sequência válida, reabertura por obstáculo, parada por tempo excedido e emergência com rearme.

O carro só avança automaticamente pelo vão depois de o portão simulado abrir. O controle não fecha apenas porque transcorreram alguns segundos após a abertura; exige passagem confirmada e vão livre. Os botões manuais permitem estudar casos sem uma sequência automática.

## Três exercícios
1. Usar Entrada automática e acompanhar os estados até o fechamento. Repetir com Saída automática.
2. Durante um fechamento, marcar Obstáculo no vão e observar a reversão do comando.
3. Reiniciar, iniciar uma entrada e, durante a abertura, marcar Falha da confirmação de posição. Aguardar a falha por tempo excedido. Retirar a falha e usar Rearmar falha. Com posição desconhecida, o controle aguarda sem movimento automático.

O botão de exportação gera JSON identificado como **simulação sem hardware**. Guardar esse arquivo se for necessário documentar um ensaio da lógica, sem apresentá-lo como medição física.

## Limites deste modelo
Não há dimensões em milímetros, cálculo de esforço ou escolha do motor. O carro é um ponto no modelo de detecção, a geometria é ilustrativa e o movimento do portão é simplificado. A localização/campo dos sensores e a segurança física exigem validação quando houver carrinho e mecanismo.

O atuador da garagem será próprio. O servo do brise e o HC-SR04 do reservatório continuam reservados às suas funções. A lógica ainda não foi portada para pinos e driver de um portão físico.

## Testes reproduzíveis
Na raiz do repositório, executar:

```sh
node 09_Simulacoes/Garagem/teste_portao.cjs
```

Resultado registrado: **16 cenários**, incluindo entrada/saída, obstáculos, tempo excedido, sensores contraditórios, parada e rearme. A lógica em `controle_portao.js` é a mesma incorporada na página HTML. Os testes não validam sensores ou mecanismo reais.
