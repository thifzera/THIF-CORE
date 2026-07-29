import threading
import time
import unittest

from core.scheduler import Scheduler


class SchedulerTests(unittest.TestCase):
    def test_schedule_and_execute_callback(self) -> None:
        scheduler = Scheduler()
        executed: list[int] = []

        def callback() -> None:
            executed.append(1)

        scheduler.schedule("tick", 0.05, callback)
        scheduler.start()
        time.sleep(0.15)
        scheduler.stop()

        self.assertTrue(executed)

    def test_cancel_and_exists(self) -> None:
        scheduler = Scheduler()
        scheduler.schedule("heartbeat", 0.1, lambda: None)

        self.assertTrue(scheduler.exists("heartbeat"))
        scheduler.cancel("heartbeat")
        self.assertFalse(scheduler.exists("heartbeat"))

    def test_list_tasks(self) -> None:
        scheduler = Scheduler()
        scheduler.schedule("first", 0.1, lambda: None)
        scheduler.schedule("second", 0.1, lambda: None)

        self.assertEqual(scheduler.list_tasks(), ["first", "second"])


if __name__ == "__main__":
    unittest.main()
