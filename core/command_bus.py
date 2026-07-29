from __future__ import annotations

from collections.abc import Callable
from typing import Any


class CommandBus:
    """Simple command dispatcher for THIF CORE."""

    def __init__(self) -> None:
        self._handlers: dict[str, Callable[..., Any]] = {}

    def register(self, command: str, handler: Callable[..., Any]) -> None:
        """Register a handler for a command name."""
        self._handlers[command] = handler

    def unregister(self, command: str) -> None:
        """Remove the handler registered for a command name."""
        if command not in self._handlers:
            raise KeyError(f"Command '{command}' is not registered")
        del self._handlers[command]

    def execute(self, command: str, *args: Any, **kwargs: Any) -> Any:
        """Execute a registered command with the provided arguments."""
        if command not in self._handlers:
            raise KeyError(f"Command '{command}' is not registered")
        return self._handlers[command](*args, **kwargs)

    def list_commands(self) -> list[str]:
        """Return the registered command names in insertion order."""
        return list(self._handlers.keys())
