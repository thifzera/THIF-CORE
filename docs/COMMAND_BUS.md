# Command Bus

## Objetivo

Documentar o barramento de comandos do THIF CORE, que centraliza o registro e execução de ações de forma independente.

## Visão Geral

O Command Bus é um componente leve e autônomo responsável por registrar handlers para comandos e executá-los quando solicitado. Ele não depende do Event Bus, do ModuleManager ou dos módulos existentes.

## Estrutura

### Comportamentos implementados
- register(command, handler): registra um handler para um comando.
- unregister(command): remove o registro de um comando.
- execute(command, *args, **kwargs): executa o handler associado.
- list_commands(): retorna os nomes dos comandos registrados.

### Fluxo básico
1. Um comando é registrado com um handler.
2. O comando é executado através do barramento.
3. O handler associado processa os argumentos recebidos.

## Exemplos

```py
from core.command_bus import CommandBus

bus = CommandBus()
bus.register("greet", lambda name: f"Hello, {name}")
print(bus.execute("greet", "THIF"))
print(bus.list_commands())
```
