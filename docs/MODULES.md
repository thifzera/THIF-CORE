# Módulos

## Objetivo

Descrever a organização dos módulos do THIF CORE e o papel de cada componente dentro do sistema.

## Visão Geral

O projeto utiliza uma arquitetura modular, onde cada módulo encapsula uma responsabilidade específica, como voz, clima, interface de fala e recursos do sistema.

## Estrutura

### Módulos principais
- Voice Module: responsável pela saída de voz e sons.
- Weather Module: responsável por integrar dados meteorológicos.
- Speech Module: responsável pela camada de fala e mensagens.
- System Module: responsável por recursos e integração com o ambiente do sistema.
- Diagnostics Module: responsável por expor informações de diagnóstico do núcleo, incluindo módulos, serviços, comandos e métricas básicas.

### Padrão de organização
Cada módulo segue uma estrutura baseada em:
- inicialização
- ciclo de vida
- shutdown
- integração com o engine

### Registro de serviços
O ModuleManager registra automaticamente cada módulo inicializado em um ServiceRegistry central, permitindo consultar o módulo por nome durante o boot e em etapas posteriores da execução.

## Exemplos

```md
### Exemplo de módulo
- Nome: voice
- Responsabilidade: emitir respostas sonoras e sons de sistema.
- Estado: inicializado, em execução ou parado.
```
