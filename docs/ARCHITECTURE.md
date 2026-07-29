# Architecture

## Objetivo

Descrever a estrutura principal do NÚCLEO THIF e a forma como os componentes internos se relacionam para manter o sistema organizado e extensível.

## Visão Geral

O núcleo é composto por um motor principal, um gerenciador de módulos, um sistema de eventos, um barramento de comandos, um registro de serviços e um scheduler interno. Essa composição permite que o projeto evolua de forma modular, sem acoplar demais os componentes.

## Estrutura

- CoreEngine: coordenador principal do ciclo de vida do sistema.
- ModuleManager: controla a inicialização, execução e encerramento dos módulos.
- EventBus: facilita a comunicação entre componentes por meio de eventos.
- CommandBus: direciona comandos para handlers específicos.
- ServiceRegistry: centraliza o registro de serviços.
- Scheduler: executa tarefas periódicas em segundo plano.

## Scheduler

### Funcionamento

O Scheduler é um componente leve responsável por executar callbacks Python periodicamente em uma thread de fundo. Ele permite registrar tarefas com nome, intervalo e função de execução.

### Ciclo de Vida

1. O scheduler é criado junto ao CoreEngine.
2. O método start() inicia a thread em segundo plano.
3. As tarefas registradas são executadas conforme o intervalo definido.
4. O método stop() encerra a execução do scheduler quando o core é parado.

### Exemplos

```py
from core.scheduler import Scheduler

scheduler = Scheduler()
scheduler.schedule("heartbeat", 1.0, lambda: print("tick"))
scheduler.start()
# ...
scheduler.stop()
```
