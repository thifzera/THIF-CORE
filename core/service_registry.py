from __future__ import annotations

from typing import Any


class ServiceRegistry:
    """Central registry for services used by THIF CORE."""

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """Register a service under the provided name."""
        self._services[name] = service

    def unregister(self, name: str) -> None:
        """Remove a service from the registry."""
        if name not in self._services:
            raise KeyError(f"Service '{name}' is not registered")
        del self._services[name]

    def get(self, name: str) -> Any:
        """Return a registered service by name."""
        if name not in self._services:
            raise KeyError(f"Service '{name}' is not registered")
        return self._services[name]

    def exists(self, name: str) -> bool:
        """Return whether a service name exists in the registry."""
        return name in self._services

    def list_services(self) -> list[str]:
        """Return the registered service names in insertion order."""
        return list(self._services.keys())
