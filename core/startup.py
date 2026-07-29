from __future__ import annotations

from pathlib import Path

from .engine import CoreEngine
from .module_manager import ModuleManager
from modules.diagnostics.module import DiagnosticsModule
from modules.speech.module import SpeechModule
from modules.system.module import SystemModule
from modules.weather.module import WeatherModule
from modules.voice.module import VoiceModule


def create_module_manager() -> ModuleManager:
    """Build a module manager with registered modules and boot order."""
    manager = ModuleManager()

    voice_module = VoiceModule()
    weather_module = WeatherModule()
    system_module = SystemModule()
    speech_module = SpeechModule()
    diagnostics_module = DiagnosticsModule(command_bus=None, service_registry=None)

    manager.register_module(voice_module)
    manager.register_module(weather_module)
    manager.register_module(system_module)
    manager.register_module(speech_module)
    manager.register_module(diagnostics_module)

    manager.enable_module(voice_module.name)
    manager.enable_module(weather_module.name)
    manager.enable_module(system_module.name)
    manager.enable_module(speech_module.name)
    manager.enable_module(diagnostics_module.name)

    manager.set_boot_order([
        voice_module.name,
        weather_module.name,
        system_module.name,
        speech_module.name,
        diagnostics_module.name,
    ])

    return manager


def initialize(config_path: str | Path | None = None) -> CoreEngine:
    """Initialize a CoreEngine instance with optional configuration."""
    module_manager = create_module_manager()
    engine = CoreEngine(config_path=config_path, module_manager=module_manager)
    engine.initialize()
    return engine


def start_engine(config_path: str | Path | None = None) -> CoreEngine:
    """Initialize and start a CoreEngine instance."""
    engine = initialize(config_path=config_path)
    engine.start()
    return engine


run = start_engine
