# Gerador de documentação R02

Fonte editável do conjunto R02, preservada nesta publicação. Requer Python 3 e as bibliotecas `reportlab` e `ezdxf`.

Em um ambiente Python com permissão de instalação, executar:

```sh
python -m pip install -r requirements.txt
python NEXUS_Gerador_Documentacao.py
```

O script contém sua própria verificação/instalação das duas bibliotecas. Conferir o diretório de saída definido no final do arquivo antes da execução. Coordenadas e parâmetros estão em milímetros da maquete; as vistas arquitetônicas usam fator 20.

Os arquivos publicados em `01_Arquitetura/R02` são os entregáveis de referência desta revisão. O gerador ainda não incorpora a garagem. A regeneração pode mudar metadados e deve ocorrer em pasta de trabalho separada para preservar a revisão apresentada.
