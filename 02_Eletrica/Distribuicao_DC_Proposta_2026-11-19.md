# Distribuição de alimentação da nova montagem

Proposta para conferência na bancada. Não é um esquema de ligação final. Primeiro ensaio: somente Mega e shield pelo USB, sem demais fontes e periféricos.

| Ramo | Fonte candidata disponível | Cargas | Conferência antes de ligar |
| --- | --- | --- | --- |
| Controle e display no ensaio inicial | USB do computador | Mega e shield | Encaixe, corrente do conjunto, estabilidade e ausência de outras fontes |
| Circuitos externos de 5 V | Fonte P4 5 V / 3 A | Sensores e iluminação compatíveis | Tensão, polaridade, corrente e queda nos fios |
| Servos | STEP POWER indicada em foto como 5 V / 4 A | MG996R e/ou SG90, conforme resultado dos testes | Modelo completo, saída real, picos e simultaneidade; corrente nominal não garante quatro servos em qualquer condição |
| Atuadores que aceitem 6 V | Fonte P4 6 V / 2 A | Apenas cargas identificadas como compatíveis | Não usar no barramento de 5 V; confirmar margem e corrente de pico |
| Cargas de 12 V | Fonte de 12 V já disponível | Bomba e fita RGB conforme suas etiquetas/interfaces | Potência disponível e acionamentos separados da lógica |

## Organização física

1. Com tudo desligado, identificar pares de alimentação e continuidade de cada trecho da protoboard. Trilhos podem ser interrompidos.
2. Marcar os ramos de 5 V, 6 V e 12 V. Não unir positivos de fontes diferentes.
3. Medir a saída de cada fonte e a polaridade do P4 antes de conectar cargas.
4. Alimentar servos e demais cargas de corrente elevada por distribuição adequada, evitando que toda sua corrente passe pelos contatos da protoboard ou por um único jumper.
5. Estabelecer GND de referência comum entre Mega, fontes DC isoladas e módulos que trocam sinais. Fazer os retornos dos motores chegarem à distribuição sem atravessar o caminho de retorno do display.
6. Acrescentar uma carga por vez e medir a tensão no seu conector durante o acionamento.

## Interfaces que exigem cuidado na remontagem

- Os pinos de sinal do Mega não são saídas de potência para motores, bomba ou fita RGB.
- Não alimentar a entrada 5V do Mega com 6 V ou 12 V. Também não aplicar 5 V em VIN esperando obter a mesma alimentação regulada.
- Uma futura alimentação externa do Mega deve ter método definido antes de conectar simultaneamente o USB. No primeiro ensaio, usar somente USB.
- Diodo em série no sinal do servo não resolve quedas na alimentação e não faz parte da proposta. Acionamento de motor DC ou bobina exige proteção própria conforme a carga; servo possui eletrônica interna e deve seguir sua interface.
- A ligação da rede às fontes com bornes expostos deve ficar protegida e fora da protoboard, realizada por integrante capacitado.
- A descrição comercial da fita é contraditória: menciona 4,8 W/m, fonte de 12 V/1 A e conteúdo branco frio/RGB. Não dimensionar a alimentação dos 5 m a partir dessa descrição. Conferir o material real e ensaiar inicialmente um trecho adequado.

## O que registrar

Modelo e tensão de cada fonte, carga ligada, tensão sem carga e durante movimento/iluminação, ocorrência de reinício e aquecimento anormal. Se aparecer a abertura NEXUS novamente, registrar o evento como possível reinício, sem concluir automaticamente que a tela queimou.
