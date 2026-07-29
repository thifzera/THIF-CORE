import unittest
from pathlib import Path

from core.config import ConfigManager
from core.engine import CoreEngine
from core.events import EventBus
from core.module_manager import BaseModule, ModuleManager


class DemoModule(BaseModule):
    def __init__(self, name: str = "demo") -> None:
        super().__init__(name=name, description="demo module")
        self.started = False
        self.stopped = False

    def start(self, engine: CoreEngine | None = None) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True


class FoundationTests(unittest.TestCase):
    def test_config_manager_reads_default_settings(self) -> None:
        config_path = Path(__file__).resolve().parents[1] / "config" / "config.json"
        manager = ConfigManager(config_path=config_path)

        self.assertEqual(manager.get("application"), "THIF CORE")
        self.assertEqual(manager.get("version"), "1.0.0-alpha")
        self.assertEqual(manager.get("logging.level", "INFO"), "INFO")

    def test_event_bus_delivers_payload_to_subscribers(self) -> None:
        bus = EventBus()
        received: list[dict[str, bool]] = []

        bus.subscribe("test.event", lambda payload: received.append(payload))
        bus.publish("test.event", {"ok": True})

        self.assertEqual(received, [{"ok": True}])

    def test_module_manager_registers_and_starts_modules(self) -> None:
        module_manager = ModuleManager()
        module = DemoModule()

        module_manager.register_module(module)
        module_manager.enable_module(module.name)
        module_manager.start_all()

        self.assertTrue(module.started)
        self.assertTrue(module_manager.get_module(module.name) is module)

    def test_engine_starts_and_stops_cleanly(self) -> None:
        engine = CoreEngine()
        module = DemoModule()
        engine.module_manager.register_module(module)
        engine.module_manager.enable_module(module.name)

        engine.start()
        self.assertTrue(engine.is_running)
        self.assertTrue(module.started)

        engine.stop()

        self.assertFalse(engine.is_running)
        self.assertFalse(module.started)
        self.assertTrue(module.stopped)


if __name__ == "__main__":
    unittest.main()
