# Nova montagem: preparação para a bancada de 20/11/2026

Revisão documental de 19/11/2026. Engenharia · UniFECAF · NEXUS.

## O que está confirmado

O novo shield TFT de 3,5 polegadas foi recebido. A compra complementar está registrada na planilha da equipe, com 49 linhas de produtos. Compra registrada, recebimento conferido e funcionamento ensaiado são estados diferentes. O inventário desta revisão registra a compra, sem atribuir aprovação física aos componentes.

O programa de demonstração do display é separado da integração R06. A compilação para Mega foi aprovada na preparação anterior; imagem, toque e alimentação do exemplar recebido ainda dependem de ensaio físico. As páginas de energia, água, acesso e clima desse programa apresentam dados ilustrativos.

## Documentos para abrir na bancada

1. [Roteiro de testes](../09_Simulacoes/Validacao/Roteiro_Bancada_2026-11-20.md).
2. [Programa e instruções do display](../07_Codigo/NEXUS_Display_Demo/README.md).
3. [Substituições e integrações](../08_BOM/Transicao_Componentes_2026-11-19.md).
4. [Distribuição de alimentação proposta](../02_Eletrica/Distribuicao_DC_Proposta_2026-11-19.md).
5. [Mapa preliminar de interfaces](../04_Automacao/Interfaces_Nova_Montagem_2026-11-19.md).
6. [Inventário da compra](../08_BOM/Compra_3_Componentes_2026-11-19.csv).
7. [Ficha de resultados para preencher](../09_Simulacoes/Validacao/Registro_Nova_Montagem_2026-11-20.csv).

## Decisões já tomadas

- Começar pelo display sozinho, com o restante desconectado.
- Trabalhar com os materiais disponíveis; esta revisão não condiciona o avanço a novas compras.
- Preservar o firmware R06 e seus registros. A mudança de display e sensores exige adaptação, não a simples troca do arquivo de pinagem antigo.
- Integrar uma função por vez depois do seu teste individual.
- Atualizar a documentação instalada após conferir as ligações e registrar os resultados reais.

## Limites desta revisão

Não há pinagem final liberada para toda a nova montagem. Não há confirmação do curso dos SG90, controlador do TFT, bateria do RTC, acessórios da fita, corrente de pico do conjunto ou compatibilidade dos níveis lógicos de cada módulo recebido. As propostas abaixo orientam a conferência e preservam as funções anteriores como referência, sem declarar novos recursos implementados.

## Ao encerrar a bancada

Salvar a versão efetivamente gravada, preencher os resultados, fotografar ligações e etiquetas das fontes, registrar o ID do TFT e os pinos/calibração do touch. Anotar qualquer alteração de pino antes de gravar o firmware integrado. Não publicar UIDs de cartões de acesso, dados pessoais ou fotografias legíveis da nota fiscal.
