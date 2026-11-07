# Compatibilização R02

NEXUS | 06/11/2026 | Conferência documental das interfaces conhecidas.

Esta matriz cruza os documentos atuais e explicita decisões que podem travar a montagem. Não constitui detecção geométrica automática, levantamento de campo ou aprovação física de interferências. A revisão de rota da pia e as reservas dos componentes são decisões já documentadas; as evidências de conclusão dos demais itens ainda não foram recebidas.

| ID | Interface | Situação encontrada | Ação concreta | Evidência para fechar | Estado |
| --- | --- | --- | --- | --- | --- |
| K01 | Plantas x garagem | Escopo funcional ainda sem geometria nas plantas | Medir carrinho/vão/mecanismo e inserir a extensão | Planta revisada com cotas e curso livre | Pendente de medidas |
| K02 | Brise x portão | Único microservo já reservado ao brise | Manter reserva e selecionar atuação própria para portão | BOM/peças sem dupla alocação | Reserva documental definida; seleção pendente |
| K03 | Água x garagem | Único HC-SR04 reservado ao reservatório | Definir detecções independentes para portão | Mapa de sensores e ensaio de passagem | Pendente de seleção |
| K04 | Luz x brise x intrusão | Um LDR e um PIR para funções compartilhadas | Integrar leitura única e distribuir eventos; testar módulos separados antes | Mapa e firmware com leitura compartilhada | Pendente de integração |
| K05 | Mega x módulos | Sketches independentes usam uma mesma placa | Não reunir .ino na mesma pasta; integrar após revisar pinos/temporização | Firmware integrado compilado e ensaiado | Pendente |
| K06 | Pinagem x garagem | Pinos do mecanismo ainda não alocados | Fechar interfaces e revisar mapa completo antes da integração | Mapa único sem conflitos | Pendente |
| K07 | Mega x ESP32/RC522 | Níveis e interfaces precisam de confirmação | Identificar placas e seguir guias; fechar interface adequada | Esquema e identificação da interface | Pendente |
| K08 | Fontes x cargas | Fontes 5/12 V e solenoide descrita 6 V | Conferir modelos, correntes e distribuição antes de selecionar | Tabela real de cargas/fontes e esquema DC | Pendente |
| K09 | Bomba/solenoide x relé | Um módulo relé não confirma canais/interfaces suficientes | Definir canais de acionamento/proteção pelas cargas | Esquema DC e ensaio de cada ramo | Pendente |
| K10 | Parada lógica x botão físico | Sketch e botão não comprovam comportamento de corte | Identificar contatos e definir resposta de cada carga | Ensaio de parada/rearme com resultados | Pendente |
| K11 | RFID x fechadura | Programa atual usa LED para autorização | Completar interface e montagem antes de declarar liberação real | Teste autorizado/recusado e retorno ao estado previsto | Pendente |
| K12 | Água x controle | Programa atual não aciona bomba e vazão não calibrada | Ensaiar leitura/calibração e circuito separado antes da atuação | Registro de nível, vazão, partida/parada e falhas | Pendente |
| K13 | Água x eletrônica | Percurso e suportes da recirculação ainda não montados | Conferir bandeja, mangueiras e acesso com módulos fora da zona molhada | Fotos e ensaio de estanqueidade em bancada | Pendente |
| K14 | Pia x sala/estrutura | Trajeto anterior atravessava sala | Usar nova rota R02 até CG1 e conferir estrutura/inspeção | Planta coordenada; referência R01 superada identificada | Rota revisada documentalmente; execução não conferida |
| K15 | Reservatórios x apoio | Reservatórios residenciais devem ficar no solo no cenário | Definir área técnica e apoio; não transferir carga à cobertura | Implantação/apoio detalhados | Pendente de implantação |
| K16 | Esgoto x ligação pública | Cotas públicas são hipotéticas | Conferir lote/rede antes de executar; revisar cotas se necessário | Levantamento e cotas revisadas | Pendente externo |
| K17 | Água potável x NP | Reposição/tratamento dependem de solução final | Manter concepção R02 e selecionar componentes compatíveis | Esquema, fichas e ensaios do conjunto | Pendente externo |
| K18 | Banhos x pontos elétricos | Volumes conferidos por box adotado 800 x 800 mm | Rever se mudar geometria; compatibilizar instalação/peças | Planta final e revisão técnica | Verificação no cenário; final pendente |
| K19 | Fotovoltaica x cobertura | Área gráfica não comprova apoio/sombra | Conferir implantação, estrutura e produtos antes da seleção final | Detalhe e fichas compatíveis | Pendente externo |
| K20 | Solar de bancada x alimentação | Painel/controlador/bateria não compatibilizados | Manter experimento separado até identificação e ensaio | Fotos, esquema e medições | Pendente |
| K21 | Câmeras x rede | OV7670 disponíveis não são câmeras IP operacionais | Definir captura e distinguir da proposta residencial | Imagem capturada e configuração reproduzível | Pendente |
| K22 | Alarmes x sensores | Simulação existe; sensores dedicados não identificados | Definir demonstração física e manter rótulo de simulação quando aplicável | Teste por evento com origem identificada | Pendente |
| K23 | Base x fechamento/transporte | Tamanho de base ainda proposto | Montagem a seco, acesso a tampas, conectores e peso/transporte | Fotos de montagem e conferência de acesso | Pendente |
| K24 | Documentos x evidências | Resultados de software não demonstram hardware | Vincular testes físicos ao código/configuração e atualizar status | Ficha preenchida com evidência e revisão | Pendente |

## Ordem prática

Primeiro resolver K01-K13 e K23 com os materiais na mesa: medidas, disponibilidade, interfaces, pinos, fontes e ensaios individuais. As verificações residenciais K14-K19 alimentam o projeto acadêmico e seu detalhamento; não são instruções para ligar a maquete em tensão residencial. K20-K22 podem continuar como estudos separados até existir uma implementação demonstrável. K24 acompanha todas as etapas.

Para fechar um item, registrar responsável, data, decisão, arquivo/foto e resultado do teste. Não atribuir responsáveis nem datas de conclusão sem confirmação da equipe. Toda alteração que mudar a planta, a pinagem ou a carga deve atualizar o documento de origem, a BOM e a ficha de ensaio correspondente.

Fontes: [arquitetura](../01_Arquitetura/R02/), [dimensionamento R02](../06_Calculos/Dimensionamento_R02/), [especificação das automações](../04_Automacao/NEXUS_Especificacao_Automacoes_R01.txt), [rede R01](../05_Seguranca/Rede_R01/), [guias de bancada](Guia_Bancada_Modulos.md) e [BOM consolidada](../08_BOM/Consolidacao_R02/).
