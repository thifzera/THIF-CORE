import tempfile
import unittest
from pathlib import Path

from core.module_manager import ModuleManager
from core.plugin_loader import PluginLoader
from core.service_registry import ServiceRegistry
from core.module_manager import BaseModule
from core.engine import CoreEngine


class DemoPluginModule(BaseModule):
    def __init__(self, name: str = "demo_plugin") -> None:
        super().__init__(name=name, description="demo plugin")

    def initialize(self, engine: CoreEngine | None = None) -> None:
        return None

    def shutdown(self) -> None:
        return None


class PluginLoaderTests(unittest.TestCase):
    def test_discover_plugins_returns_available_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            plugins_dir = Path(temp_dir)
            (plugins_dir / "sample_plugin.py").write_text("PLUGIN = object()\n", encoding="utf-8")
            loader = PluginLoader(plugins_dir=plugins_dir)

            self.assertEqual(loader.discover_plugins(), ["sample_plugin"])

    def test_load_plugins_ignores_invalid_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            plugins_dir = Path(temp_dir)
            (plugins_dir / "broken_plugin.py").write_text("raise RuntimeError('boom')\n", encoding="utf-8")
            loader = PluginLoader(plugins_dir=plugins_dir)

            loaded = loader.load_plugins()

            self.assertEqual(loaded, [])

    def test_load_plugins_registers_modules_and_services(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            plugins_dir = Path(temp_dir)
            plugin_code = "from core.module_manager import BaseModule\nfrom core.engine import CoreEngine\n\nclass SamplePlugin(BaseModule):\n    def __init__(self):\n        super().__init__(name='sample_plugin', description='demo')\n    def initialize(self, engine: CoreEngine | None = None) -> None:\n        return None\n    def shutdown(self) -> None:\n        return None\n\nPLUGIN = SamplePlugin()\n"
            (plugins_dir / "sample_plugin.py").write_text(plugin_code, encoding="utf-8")
            loader = PluginLoader(plugins_dir=plugins_dir)
            manager = ModuleManager(service_registry=ServiceRegistry())
            registry = manager.service_registry

            loader.load_plugins(module_manager=manager, service_registry=registry)

            self.assertEqual(loader.list_plugins(), ["sample_plugin"])
            self.assertTrue(registry.exists("sample_plugin"))


if __name__ == "__main__":
    unittest.main()
