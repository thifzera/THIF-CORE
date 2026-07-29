from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigManager:
    """Load and manage application configuration."""

    def __init__(self, config_path: str | Path | None = None, defaults: dict[str, Any] | None = None) -> None:
        self.config_path = Path(config_path or Path(__file__).resolve().parents[1] / "config" / "config.json")
        self.defaults = dict(defaults or {})
        self._data: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load configuration from the JSON file and apply defaults."""
        self._data = dict(self.defaults)
        self._data.setdefault("application", "THIF CORE")
        self._data.setdefault("version", "0.1.0")
        self._data.setdefault("logging", {"level": "INFO"})

        if self.config_path.exists():
            with self.config_path.open("r", encoding="utf-8") as handle:
                loaded = json.load(handle)
            if isinstance(loaded, dict):
                self._data.update(loaded)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key, supporting dot notation."""
        if "." in key:
            current: Any = self._data
            for part in key.split("."):
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return default
            return current
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value by key, supporting dot notation."""
        if "." in key:
            parts = key.split(".")
            target: dict[str, Any] = self._data
            for part in parts[:-1]:
                next_value = target.get(part)
                if not isinstance(next_value, dict):
                    next_value = {}
                    target[part] = next_value
                target = next_value
            target[parts[-1]] = value
        else:
            self._data[key] = value

    def save(self) -> None:
        """Persist the current configuration to disk."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with self.config_path.open("w", encoding="utf-8") as handle:
            json.dump(self._data, handle, indent=2)
            handle.write("\n")
