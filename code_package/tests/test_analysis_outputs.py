import unittest
from pathlib import Path
import tempfile

from dlgpr.experiment import ExperimentConfig, run_suite
from dlgpr.analysis import analyze


class TestAnalysisOutputs(unittest.TestCase):
    def test_additional_tables_exist(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cfg = ExperimentConfig(tasks=["line-duel"], seeds=[0], intervals=2)
            methods = ["DLGPR-full", "fixed-split", "round-robin", "greedy-improvement", "no-handshake", "strict-delta-max", "relaxed-delta-min"]
            run_suite(cfg, methods, root / "logs")
            outputs = analyze(root / "logs", root / "tables", root / "figures")
            for key in ["scheduler_baselines", "method_equivalence", "metric_definitions", "claim_limits", "stats"]:
                self.assertIn(key, outputs)
                self.assertTrue(outputs[key].exists())
            main_text = outputs["main"].read_text(encoding="utf-8")
            stats_text = outputs["stats"].read_text(encoding="utf-8")
            equivalence_text = outputs["method_equivalence"].read_text(encoding="utf-8")
            self.assertIn("return_median_up", main_text)
            self.assertIn("comparator_median", stats_text)
            self.assertIn("DLGPR-full", equivalence_text)
            self.assertIn("strict-delta-max", equivalence_text)
            self.assertIn("fixed-split", equivalence_text)
            self.assertIn("round-robin", equivalence_text)


if __name__ == "__main__":
    unittest.main()
