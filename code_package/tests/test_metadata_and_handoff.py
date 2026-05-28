import unittest
from pathlib import Path
import tempfile
import json
import pandas as pd

from dlgpr.experiment import ExperimentConfig, run_suite
from dlgpr.external_adapters import validate_adapter_metadata
from dlgpr.envs import make_env


class TestMetadataAndHandoff(unittest.TestCase):
    def test_metadata_complete(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = ExperimentConfig(tasks=["line-duel"], seeds=[0], intervals=2)
            run_suite(cfg, ["DLGPR-full"], Path(td))
            meta = json.loads((Path(td) / "environment_metadata.json").read_text())
            item = meta["tasks"]["line-duel"]
            required = [
                "environment_name", "environment_version", "benchmark_family", "task_name",
                "observation_definition", "action_definition", "reward_definition",
                "episode_termination", "opponent_policy", "stochasticity_sources",
                "training_seed_schedule", "evaluation_seed_schedule", "rollout_horizon_H",
                "number_of_rollouts_K", "B_tau_ms", "delta_min_ms", "delta_max_ms",
                "guard_margin_ms", "evaluation_cadence", "timing_mode",
            ]
            self.assertFalse([k for k in required if k not in item or item[k] in (None, "")])

    def test_cross_layer_handoff_ablation_is_real(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = ExperimentConfig(tasks=["line-duel"], seeds=[0], intervals=3)
            run_suite(cfg, ["DLGPR-full", "no-handshake"], Path(td))
            df = pd.read_csv(Path(td) / "interval_logs.csv")
            sums = df.groupby("method")["handshake_events"].sum().to_dict()
            self.assertGreater(sums.get("DLGPR-full", 0), 0)
            self.assertEqual(sums.get("no-handshake", -1), 0)

    def test_adapter_metadata_validator(self):
        env = make_env("line-duel", seed=0)
        checklist = validate_adapter_metadata(env.metadata)
        self.assertTrue(checklist.complete())


if __name__ == "__main__":
    unittest.main()
