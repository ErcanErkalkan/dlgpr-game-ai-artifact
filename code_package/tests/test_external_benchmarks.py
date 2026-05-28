import unittest

import numpy as np

from dlgpr.envs import make_env
from dlgpr.external_adapters import validate_adapter_metadata


class TestExternalBenchmarks(unittest.TestCase):
    def test_gymnasium_tasks_have_complete_metadata(self):
        for task in [
            "gym-frozenlake-4x4",
            "gym-frozenlake-4x4-deterministic",
            "gym-cliffwalking",
            "gym-blackjack",
            "minigrid-empty-5x5",
        ]:
            with self.subTest(task=task):
                env = make_env(task, seed=0)
                obs = env.reset(0)
                self.assertEqual(obs.shape[0], env.obs_dim)
                self.assertEqual(env.action_dim, env.metadata.action_space_size)
                self.assertTrue(np.isfinite(obs).all())
                self.assertTrue(validate_adapter_metadata(env.metadata).complete())

    def test_gymnasium_step_contract(self):
        for task in [
            "gym-frozenlake-4x4",
            "gym-frozenlake-4x4-deterministic",
            "gym-cliffwalking",
            "gym-blackjack",
            "minigrid-empty-5x5",
        ]:
            with self.subTest(task=task):
                env = make_env(task, seed=1)
                env.reset(1)
                obs, reward, done, info = env.step(0)
                self.assertEqual(obs.shape[0], env.obs_dim)
                self.assertIsInstance(float(reward), float)
                self.assertIsInstance(done, bool)
                self.assertIn("win", info)


if __name__ == "__main__":
    unittest.main()
