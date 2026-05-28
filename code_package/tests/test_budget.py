import unittest
from pathlib import Path
import tempfile
import pandas as pd
from dlgpr.experiment import ExperimentConfig, run_suite


class TestBudget(unittest.TestCase):
    def test_strict_has_no_loop_overrun_in_smoke(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = ExperimentConfig(tasks=["line-duel"], seeds=[0], intervals=3, B_tau_ms=24, guard_margin_ms=2, delta_min_ms=1, delta_max_ms=4)
            run_suite(cfg, ["strict-delta-max"], Path(td))
            df = pd.read_csv(Path(td) / "interval_logs.csv")
            self.assertEqual(int(df["loop_overrun"].sum()), 0)

    def test_logs_have_required_columns(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = ExperimentConfig(tasks=["line-duel"], seeds=[0], intervals=2)
            run_suite(cfg, ["DLGPR-full"], Path(td))
            df = pd.read_csv(Path(td) / "interval_logs.csv")
            for col in ["environment_name", "score", "return", "p99_latency_ms", "do_not_start_rule"]:
                self.assertIn(col, df.columns)


if __name__ == "__main__":
    unittest.main()
