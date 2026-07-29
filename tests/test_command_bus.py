import unittest

from core.command_bus import CommandBus


class CommandBusTests(unittest.TestCase):
    def test_register_and_execute_command(self) -> None:
        bus = CommandBus()
        calls: list[tuple[str, tuple[object, ...], dict[str, object]]] = []

        def handler(name: str, *, suffix: str = "") -> str:
            calls.append((name, (), {"suffix": suffix}))
            return f"{name}{suffix}"

        bus.register("greet", handler)

        self.assertEqual(bus.execute("greet", "THIF", suffix="!"), "THIF!")
        self.assertEqual(calls[0][0], "THIF")

    def test_unregister_removes_command(self) -> None:
        bus = CommandBus()
        bus.register("ping", lambda: "pong")

        bus.unregister("ping")

        with self.assertRaises(KeyError):
            bus.execute("ping")

    def test_list_commands_returns_registered_names(self) -> None:
        bus = CommandBus()
        bus.register("alpha", lambda: None)
        bus.register("beta", lambda: None)

        self.assertEqual(bus.list_commands(), ["alpha", "beta"])

    def test_execute_raises_for_unknown_command(self) -> None:
        bus = CommandBus()

        with self.assertRaises(KeyError):
            bus.execute("missing")


if __name__ == "__main__":
    unittest.main()
