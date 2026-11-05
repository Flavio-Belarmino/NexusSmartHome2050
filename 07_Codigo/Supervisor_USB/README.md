# Supervisor USB local

Casa Inteligente | NEXUS | ExpoTech. R01, 05/11/2026. Programa Python para visualizar a saída de **um módulo de bancada por vez** e guardar CSV. Não envia comandos à placa e não depende do ESP32.

## Experimentar agora, sem placa

Nesta pasta, com Python 3 instalado:

```sh
python supervisor.py --demo
```

Abrir `http://127.0.0.1:8765` no mesmo computador. A página identifica **DEMONSTRAÇÃO**, com valores de exemplo. Isso testa o programa de supervisão, sem comprovar funcionamento de sensores. Encerrar com Ctrl+C no terminal.

## Receber dados da placa depois

```sh
python -m pip install -r requirements.txt
python supervisor.py --listar-portas
python supervisor.py --porta COM3 --csv registros/ensaio.csv
```

`COM3` é apenas exemplo: substituir pela porta que a listagem indicar. No Linux pode ser uma porta `/dev/tty...`. Carregar antes o sketch escolhido e fechar o Monitor Serial do Arduino IDE, pois os dois programas normalmente não podem usar a mesma porta simultaneamente. A velocidade padrão é 115200.

O programa aceita os quadros JSON de A02, A03, A04, A05, A08 e A09 e a linha de estado do A01. Textos de ajuda são ignorados. Cada cartão mostra o último quadro recebido e sua idade; uma leitura antiga não significa que o estado continue igual. Falha de DHT não é convertida em temperatura zero.

O CSV registra horário de recebimento em UTC, origem, módulo e quadro recebido. Para o modo de exemplo, o campo de origem continua DEMONSTRACAO. Não trocar esse rótulo para apresentar os dados como leitura física.

O servidor escuta apenas em `127.0.0.1`, no próprio computador, e não publica informações na internet. A comunicação Mega/ESP32 e o painel via Wi-Fi permanecem como próxima etapa, depois de identificar a placa ESP32 e definir as interfaces de 5 V/3,3 V.

## Testes

```sh
python -m unittest teste_supervisor.py
```

Testam interpretação, rejeição de quadros inválidos, origem dos registros, CSV e resposta HTTP local. Não testam uma porta USB real. A dependência serial é [pyserial](https://pyserial.readthedocs.io/en/latest/shortintro.html), versão fixada em requirements.txt.
