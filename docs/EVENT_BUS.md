# Event Bus

## Objetivo

Documentar o mecanismo de comunicação por eventos usado pelo núcleo THIF.

## Visão Geral

O Event Bus permite que diferentes componentes se comuniquem de forma desacoplada, publicando eventos e registrando handlers para respondê-los.

## Estrutura

### Componentes principais
- Publisher: publica um evento com um payload.
- Subscriber: registra uma função para receber eventos.
- Event name: identificador único do evento.

### Fluxo básico
1. Um módulo publica um evento.
2. O Event Bus encontra os subscribers registrados.
3. Cada handler processa o payload recebido.

## Exemplos

```py
event_bus.publish("engine.started", {"engine": engine})
```
