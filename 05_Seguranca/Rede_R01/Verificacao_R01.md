# Verificação de rede e segurança R01

Data: 05/11/2026. Não houve ensaio físico.

| Conferência | Resultado |
| --- | --- |
| Geometria | Referências internas dentro dos ambientes; AC01/PR01 preservados da R02 nos três eixos |
| Rede | 7 enlaces em estrela; 71,450 m geométricos sem folgas/patchcords; não é lista de compra |
| Lógica virtual | 18 cenários de teste Node.js passaram |
| HTML/JavaScript | Sintaxe JS e unicidade dos IDs estáticos conferidas; interface visual não ensaiada, pois o navegador de teste bloqueou a abertura de arquivo local |
| PDF | 4 páginas A3 renderizadas e inspecionadas; identificadores separados dos nomes dos ambientes |
| ZIP | Arquivo íntegro e seus três arquivos iguais às fontes publicadas |
| RS01_Rede_Dados.dxf | 58 entidades; 0 erros e 0 correções no ezdxf |
| RS02_Seguranca.dxf | 55 entidades; 0 erros e 0 correções no ezdxf |

Os testes não validam sensores, vídeo, autenticação, rede, atuação física, cobertura de detecção ou proteção de pessoas. Não há protocolo MQTT/ponte implementado. O contrato JSON é apenas proposta futura.

## SHA-256 dos artefatos verificados

```text
02a4c8860ef25cc0b9e295a4a52d6b8cbe028e370599b0ea9fd9f62ed839f8be  Gerar_Rede.py
db28857f7071f825807d192fc79be67f04da8149427e78a2f19e4fe31b5d8dcb  NEXUS_Rede_Seguranca_R01.pdf
35435acb9b4538f83a364d1029ec527e3eff2183e3adc87912fb80f5aea80a40  RS01_Rede_Dados.dxf
c2d858b0db229e495905dc9e2f8333e71585887642f6c70fa56025d486cb5b67  RS02_Seguranca.dxf
3272c3e7349d4bb94524bfa8ec4e02ad5ca810d9fdee0bf12448844cc19b8f89  Controle_Alarmes.js
e223b07fb0a53669292716af12fa372c224ec46addb3b771725d8d8d82da00ef  Testar_Alarmes.cjs
236ec76f7b2dd9eff4393fd24e44db2d48f300924ce5f99799e7f32a151b259a  Simulador_Alarmes.html
f98e7bde0871873fd3026592afbed62559c143cfc1a05a4f5a2d76e8d6170080  NEXUS_Simulador_Alarmes_R01.zip
1c06b4e4a6365a5530e2608e6682f36fdf3e113546a7aca8075e65ae2056db96  Pontos_Rede_Seguranca_mm.csv
4cc38fdebffba1c0cff4b6ada8424550040e9b5b9c6e74aad6a308e1fa6480da  Cabos_Dados_Estimativa.csv
8e524cc2a2e33d9aeee7c2f83b9a152980c732bdca2848f90bfe796a278dd94f  Contrato_Telemetria_Proposto.json
```
