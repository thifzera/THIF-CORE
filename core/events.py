from __future__ import annotations

from collections.abc import Callable
from typing import Any


class EventBus:
    """Simple publish/subscribe mechanism for internal app events."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[Any], None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[Any], None]) -> None:
        """Subscribe a handler to a named event."""
        self._subscribers.setdefault(event_name, []).append(handler)

    def publish(self, event_name: str, payload: Any = None) -> None:
        """Publish payload to all subscribers of the named event."""
        for handler in self._subscribers.get(event_name, []):
            handler(payload)
