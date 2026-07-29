import unittest

from core.service_registry import ServiceRegistry


class ServiceRegistryTests(unittest.TestCase):
    def test_register_and_get_service(self) -> None:
        registry = ServiceRegistry()
        registry.register("weather", {"provider": "openweather"})

        self.assertTrue(registry.exists("weather"))
        self.assertEqual(registry.get("weather"), {"provider": "openweather"})

    def test_unregister_removes_service(self) -> None:
        registry = ServiceRegistry()
        registry.register("speech", object())

        registry.unregister("speech")

        self.assertFalse(registry.exists("speech"))
        with self.assertRaises(KeyError):
            registry.get("speech")

    def test_list_services_returns_registered_names(self) -> None:
        registry = ServiceRegistry()
        registry.register("alpha", object())
        registry.register("beta", object())

        self.assertEqual(registry.list_services(), ["alpha", "beta"])


if __name__ == "__main__":
    unittest.main()
