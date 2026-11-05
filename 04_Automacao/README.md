# Automação

A [especificação R01](NEXUS_Especificacao_Automacoes_R01.pdf) define iluminação, brise, acesso RFID, monitoramento ambiental, água/nível, experimento solar, garagem e supervisão. A [versão em texto](NEXUS_Especificacao_Automacoes_R01.txt) facilita a revisão.

São regras propostas para implementação. O [primeiro firmware A01](../07_Codigo/NEXUS_A01_Bancada/README.md) está disponível para ensaio de iluminação na bancada; sua validação física e a integração dos demais módulos continuam pendentes. A pinagem R02 é preliminar e não contempla a alocação específica da garagem.

O [kit de módulos R02](../10_Documentacao/Guia_Bancada_Modulos.md) acrescenta os demais sketches de bancada, o supervisor USB e a simulação da garagem. As [interfaces e regras de integração](Interfaces_e_Integracao.md) indicam pinos, prioridades e limites. Os atuadores de bomba/fechadura ainda não são energizados pelos programas publicados.

O portão prevê inicialização, fechado, abrindo, aberto, fechando e falha/emergência. O fechamento depende da passagem confirmada e do vão livre, com interrupção/reabertura em caso de obstáculo. As funções de detecção externa, interna e de vão devem ser definidas junto ao mecanismo. Prever retorno de posição e atuador próprio.

O servo do brise e o HC-SR04 do reservatório permanecem nas funções previstas. Componentes adicionais serão especificados conforme os ensaios e as medidas do conjunto.
