import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).parents[1] / "src" / "summarize_fallbacks.py"
SPEC = importlib.util.spec_from_file_location("summarize_fallbacks", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SummarizeFallbacksTest(unittest.TestCase):
    def test_synthetic_example(self):
        sample = Path(__file__).parents[1] / "examples" / "sample_tracks.geojson"
        summary = MODULE.summarize_file(sample)
        self.assertEqual(summary["feature_count"], 2)
        self.assertEqual(summary["unique_track_count"], 2)
        self.assertEqual(summary["fallback_track_count"], 1)
        self.assertEqual(summary["fallback_track_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()

