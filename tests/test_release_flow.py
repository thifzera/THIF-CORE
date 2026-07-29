import unittest
from pathlib import Path

from core.engine import CoreEngine
from modules.speech.module import SpeechModule


class ReleaseFlowTests(unittest.TestCase):
    def test_speech_sequence_uses_config_values(self) -> None:
        config_path = Path(__file__).resolve().parents[1] / "config" / "config.json"
        engine = CoreEngine(config_path=config_path)
        engine.initialize()
        module = SpeechModule()

        sequence = module.build_sequence(engine)

        self.assertIn("THIF", sequence)
        self.assertIn("São Paulo", sequence)
        self.assertIn("teste", sequence)


if __name__ == "__main__":
    unittest.main()
