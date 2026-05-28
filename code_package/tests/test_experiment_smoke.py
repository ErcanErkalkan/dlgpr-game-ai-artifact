import unittest
from pathlib import Path
import tempfile
from dlgpr.experiment import ExperimentConfig, run_suite
from dlgpr.analysis import analyze


class TestExperimentSmoke(unittest.TestCase):
    def test_run_and_analyze(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = ExperimentConfig(tasks=["line-duel"], seeds=[0], intervals=2)
            run_suite(cfg, ["DLGPR-full", "GA-only", "strict-delta-max", "relaxed-delta-min"], root / "logs")
            outputs = analyze(root / "logs", root / "tables", root / "figures")
            self.assertTrue(outputs["main"].exists())
            self.assertTrue((root / "figures").exists())


if __name__ == "__main__":
    unittest.main()
