# Testes de lógica A01

Teste em computador, independente da placa. Para executar a partir da raiz do repositório:

```sh
g++ -std=c++11 -Wall -Wextra -Werror -pedantic 07_Codigo/Testes_A01/teste_logica.cpp -o /tmp/nexus_a01_teste
/tmp/nexus_a01_teste
```

Resultado de 05/11/2026: **28 verificações passaram**. A ficha de ensaio físico permanece sem resultados. O arquivo de teste fica fora da pasta do sketch para não ser compilado como firmware pelo Arduino IDE.

A compilação do firmware para ATmega2560 também foi concluída em 05/11/2026. O [registro de validação em computador](Validacao_Computador.md) identifica ferramentas, alvo e consumo de memória. Compilação e testes de decisão não comprovam o funcionamento físico dos sensores.
