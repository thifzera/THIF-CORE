from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

from .service_registry import ServiceRegistry

if TYPE_CHECKING:
    from .engine import CoreEngine


class ModuleState(Enum):
    NOT_LOADED = "not_loaded"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


class BaseModule(ABC):
    """Base abstraction for all application modules."""

    def __init__(
        self,
        name: str,
        version: str = "0.0.1",
        description: str = "",
        author: str = "unknown",
        dependencies: list[str] | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.dependencies = dependencies or []
        self.enabled = False
        self.started = False
        self.state = ModuleState.NOT_LOADED
        self.logger = logger or logging.getLogger(name)

    @abstractmethod
    def initialize(self, engine: CoreEngine | None = None) -> None:
        """Initialize the module before it enters the running state."""
        raise NotImplementedError

    def start(self, engine: CoreEngine | None = None) -> None:
        """Initialize and activate the module in the current engine context."""
        if self.state in (ModuleState.NOT_LOADED, ModuleState.STOPPED):
            try:
                self.initialize(engine)
                self.state = ModuleState.INITIALIZED
            except Exception as error:
                self.state = ModuleState.ERROR
                self.logger.error("Module %s failed to initialize: %s", self.name, error)
                return

        if self.state == ModuleState.INITIALIZED:
            self.state = ModuleState.RUNNING
            self.started = True

    def stop(self) -> None:
        """Stop the module and release runtime resources."""
        if self.state != ModuleState.RUNNING:
            return

        try:
            self.shutdown()
            self.state = ModuleState.STOPPED
            self.started = False
        except Exception as error:
            self.state = ModuleState.ERROR
            self.logger.error("Module %s failed to shutdown: %s", self.name, error)

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the module and cleanup resources."""
        raise NotImplementedError

    def status(self) -> ModuleState:
        """Return the current lifecycle state for the module."""
        return self.state


class ModuleManager:
    """Register and manage the lifecycle of modules."""

    def __init__(self, boot_order: list[str] | None = None, service_registry: ServiceRegistry | None = None) -> None:
        self._modules: dict[str, BaseModule] = {}
        self._module_order: list[str] = []
        self._boot_order: list[str] | None = boot_order
        self.service_registry = service_registry or ServiceRegistry()

    def register_module(self, module: BaseModule) -> None:
        """Register a module instance for later activation."""
        if module.name in self._modules:
            return
        self._modules[module.name] = module
        self._module_order.append(module.name)
        self.service_registry.register(module.name, module)

    def set_boot_order(self, order: list[str]) -> None:
        """Configure module startup order for future boot sequence customization."""
        missing = [name for name in order if name not in self._modules]
        if missing:
            raise KeyError(f"Unknown modules in boot order: {', '.join(missing)}")
        self._boot_order = order

    def enable_module(self, name: str) -> BaseModule:
        """Mark a registered module as enabled."""
        module = self.get_module(name)
        if module is None:
            raise KeyError(f"Module '{name}' is not registered")
        module.enabled = True
        return module

    def disable_module(self, name: str) -> None:
        """Disable a registered module."""
        module = self.get_module(name)
        if module is None:
            raise KeyError(f"Module '{name}' is not registered")
        module.enabled = False

    def get_module(self, name: str) -> BaseModule | None:
        """Return a registered module by name."""
        return self._modules.get(name)

    def _ordered_modules(self) -> list[BaseModule]:
        order = self._boot_order or self._module_order
        return [self._modules[name] for name in order if name in self._modules]

    def start_all(self, engine: CoreEngine | None = None) -> None:
        """Start all enabled modules in configured order."""
        for module in self._ordered_modules():
            if module.enabled and not module.started:
                module.start(engine)
                if self.service_registry.exists(module.name):
                    self.service_registry.register(module.name, module)

    def boot(self, engine: CoreEngine) -> None:
        """Execute the boot sequence through the module manager."""
        engine.logger.info("Inicializando Core")
        engine.event_bus.publish("engine.started", {"engine": engine})
        self.start_all(engine)
        engine.logger.info("Todos os módulos carregados.")
        engine.event_bus.publish("boot.sequence.completed", {"engine": engine})
        engine.logger.info("Finalizando inicialização")

    def stop_all(self) -> None:
        """Stop all started modules in reverse registration order."""
        for module in reversed(self._ordered_modules()):
            if module.started:
                module.stop()
