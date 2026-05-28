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
            for col in [
                "environment_name", "score", "return", "p99_latency_ms", "do_not_start_rule",
                "actual_cpu_loop_wall_ms", "actual_cpu_e2e_ms", "wall_clock_interval_ms",
                "actual_cpu_loop_overrun", "actual_cpu_e2e_overrun",
            ]:
                self.assertIn(col, df.columns)

    def test_actual_cpu_raw_timing_mode_is_logged(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = ExperimentConfig(tasks=["line-duel"], seeds=[0], intervals=2, timing_mode="actual_cpu_raw")
            run_suite(cfg, ["strict-delta-max"], Path(td))
            df = pd.read_csv(Path(td) / "interval_logs.csv")
            atomic = pd.read_csv(Path(td) / "atomic_step_logs.csv")
            self.assertEqual(set(df["timing_mode"]), {"actual_cpu_raw"})
            self.assertTrue((atomic["charged_ms"] >= 0).all())
            self.assertTrue((atomic["cpu_ms"] >= 0).all())


if __name__ == "__main__":
    unittest.main()
