from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from .logger import get_logger
from .module_manager import ModuleManager
from .service_registry import ServiceRegistry


class PluginLoader:
    """Discover and load plugins from the plugins directory."""

    def __init__(self, plugins_dir: str | Path | None = None, logger: Any | None = None) -> None:
        self.plugins_dir = Path(plugins_dir or Path(__file__).resolve().parents[1] / "plugins")
        self.logger = logger or get_logger(name="thif_core.plugins")
        self._loaded_plugins: dict[str, ModuleType] = {}
        self._loaded_names: list[str] = []

    def discover_plugins(self) -> list[str]:
        """Discover plugin modules in the plugins directory."""
        if not self.plugins_dir.exists():
            return []

        plugins: list[str] = []
        for path in sorted(self.plugins_dir.glob("*.py")):
            if path.name.startswith("_"):
                continue
            plugins.append(path.stem)
        return plugins

    def load_plugins(self, module_manager: ModuleManager | None = None, service_registry: ServiceRegistry | None = None) -> list[str]:
        """Load discovered plugins and register modules/services when possible."""
        loaded: list[str] = []
        for plugin_name in self.discover_plugins():
            try:
                module = self._import_plugin(plugin_name)
                self._loaded_plugins[plugin_name] = module
                self._loaded_names.append(plugin_name)
                loaded.append(plugin_name)

                if module_manager is not None:
                    module_obj = getattr(module, "PLUGIN", None)
                    if module_obj is not None:
                        module_manager.register_module(module_obj)
                        module_manager.enable_module(module_obj.name)
                        if service_registry is not None:
                            service_registry.register(module_obj.name, module_obj)

                if service_registry is not None:
                    service_registry.register(f"plugin.{plugin_name}", module)
            except Exception as error:  # pragma: no cover - defensive path
                self.logger.error("Failed to load plugin '%s': %s", plugin_name, error)
        return loaded

    def unload_plugin(self, name: str) -> None:
        """Unload a previously loaded plugin if present."""
        if name not in self._loaded_plugins:
            raise KeyError(f"Plugin '{name}' is not loaded")
        del self._loaded_plugins[name]
        if name in self._loaded_names:
            self._loaded_names.remove(name)
        sys.modules.pop(f"plugins.{name}", None)

    def list_plugins(self) -> list[str]:
        """List the successfully loaded plugin names."""
        return list(self._loaded_plugins.keys())

    def _import_plugin(self, name: str) -> ModuleType:
        module_name = f"plugins.{name}"
        if module_name in sys.modules:
            return sys.modules[module_name]

        spec = importlib.util.spec_from_file_location(module_name, self.plugins_dir / f"{name}.py")
        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to import plugin '{name}'")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
