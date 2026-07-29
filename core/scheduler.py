from __future__ import annotations

import threading
import time
from collections.abc import Callable
from typing import Any


class Scheduler:
    """Simple background scheduler for THIF CORE."""

    def __init__(self) -> None:
        self._tasks: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._running = False
        self._thread: threading.Thread | None = None

    def schedule(self, name: str, interval: float, callback: Callable[[], Any]) -> None:
        """Register or replace a periodic task."""
        with self._lock:
            self._tasks[name] = {"interval": interval, "callback": callback, "last_run": None}

    def cancel(self, name: str) -> None:
        """Remove a scheduled task by name."""
        with self._lock:
            if name not in self._tasks:
                raise KeyError(f"Task '{name}' is not scheduled")
            del self._tasks[name]

    def exists(self, name: str) -> bool:
        """Return whether a task exists."""
        with self._lock:
            return name in self._tasks

    def list_tasks(self) -> list[str]:
        """List the registered task names."""
        with self._lock:
            return list(self._tasks.keys())

    def start(self) -> None:
        """Start the background scheduler thread if it is not already running."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the scheduler and wait for the background thread to finish."""
        if not self._running:
            return
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None

    def _run_loop(self) -> None:
        while self._running:
            with self._lock:
                tasks = list(self._tasks.items())
            for name, task in tasks:
                if not self._running:
                    break
                callback = task["callback"]
                interval = float(task["interval"])
                last_run = task["last_run"]
                now = time.time()
                if last_run is None or now - last_run >= interval:
                    try:
                        callback()
                    except Exception:
                        pass
                    with self._lock:
                        if name in self._tasks:
                            self._tasks[name]["last_run"] = time.time()
            time.sleep(0.1)
