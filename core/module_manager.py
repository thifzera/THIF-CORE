from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import CoreEngine


class BaseModule(ABC):
    """Base abstraction for all application modules."""

    def __init__(self, name: str, description: str = "") -> None:
        self.name = name
        self.description = description
        self.enabled = False
        self.started = False

    @abstractmethod
    def start(self, engine: CoreEngine | None = None) -> None:
        """Start the module with an optional engine reference."""
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """Stop the module and release resources."""
        raise NotImplementedError


class ModuleManager:
    """Register and manage the lifecycle of modules."""

    def __init__(self) -> None:
        self._modules: dict[str, BaseModule] = {}

    def register_module(self, module: BaseModule) -> None:
        """Register a module instance for later activation."""
        self._modules[module.name] = module

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

    def start_all(self, engine: CoreEngine | None = None) -> None:
        """Start all enabled modules."""
        for module in self._modules.values():
            if module.enabled and not module.started:
                module.start(engine)
                module.started = True

    def stop_all(self) -> None:
        """Stop all started modules in reverse registration order."""
        for module in reversed(list(self._modules.values())):
            if module.started:
                module.stop()
                module.started = False
