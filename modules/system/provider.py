from __future__ import annotations

import logging
import platform
import shutil
import socket
import sys


class SystemProvider:
    """Provide basic system information from the current host."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger("thif_core.system.provider")

    def collect(self) -> dict[str, str | int | float]:
        """Collect current system information."""
        self.logger.info("Collecting system information")
        try:
            cpu = platform.processor() or "unknown"
            memory_total = shutil.disk_usage(".").total if hasattr(shutil, "disk_usage") else 0
            disk = shutil.disk_usage(".") if hasattr(shutil, "disk_usage") else None
            disk_total = disk.total if disk is not None else 0
            system = platform.system()
            release = platform.release()
            node = socket.gethostname()
            python_version = sys.version.split("\n", 1)[0]

            return {
                "cpu": cpu,
                "memory_total": memory_total,
                "disk_total": disk_total,
                "system": system,
                "release": release,
                "hostname": node,
                "python_version": python_version,
            }
        except Exception as error:
            self.logger.error("SystemProvider failed to collect system info: %s", error)
            return {}
