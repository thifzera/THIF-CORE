import unittest

from core.command_bus import CommandBus
from core.module_manager import ModuleManager
from core.service_registry import ServiceRegistry
from modules.diagnostics.module import DiagnosticsModule


class DiagnosticsModuleTests(unittest.TestCase):
    def test_reports_core_diagnostics(self) -> None:
        command_bus = CommandBus()
        service_registry = ServiceRegistry()
        module = DiagnosticsModule(command_bus=command_bus, service_registry=service_registry)

        module.initialize(engine=None)

        status = module.get_status()

        self.assertIn("core_version", status)
        self.assertIn("modules_loaded", status)
        self.assertIn("services_registered", status)
        self.assertIn("commands_registered", status)
        self.assertIn("uptime_seconds", status)
        self.assertIn("memory_usage_mb", status)
        self.assertIn("cpu_usage_percent", status)

        self.assertEqual(command_bus.execute("diagnostics.status"), status)

    def test_module_registers_itself_in_services_and_commands(self) -> None:
        command_bus = CommandBus()
        service_registry = ServiceRegistry()
        module = DiagnosticsModule(command_bus=command_bus, service_registry=service_registry)
        module.initialize(engine=None)

        self.assertTrue(service_registry.exists("diagnostics"))
        self.assertIn("diagnostics.status", command_bus.list_commands())

    def test_module_manager_registers_diagnostics_module(self) -> None:
        manager = ModuleManager(service_registry=ServiceRegistry())
        module = DiagnosticsModule()

        manager.register_module(module)

        self.assertTrue(manager.service_registry.exists(module.name))


if __name__ == "__main__":
    unittest.main()
