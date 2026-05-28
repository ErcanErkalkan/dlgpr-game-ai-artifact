import unittest
import numpy as np
from dlgpr.envs import make_env


class TestEnvs(unittest.TestCase):
    def test_line_duel_step(self):
        env = make_env("line-duel", seed=1)
        obs = env.reset(1)
        self.assertEqual(obs.shape[0], env.obs_dim)
        obs2, reward, done, info = env.step(1)
        self.assertEqual(obs2.shape[0], env.obs_dim)
        self.assertIsInstance(reward, float)
        self.assertIn("win", info)

    def test_grid_treasure_step(self):
        env = make_env("grid-treasure", seed=1)
        obs = env.reset(1)
        self.assertEqual(obs.shape[0], env.obs_dim)
        obs2, reward, done, info = env.step(0)
        self.assertEqual(obs2.shape[0], env.obs_dim)
        self.assertIsInstance(done, bool)

    def test_resource_defense_step(self):
        env = make_env("resource-defense", seed=1)
        obs = env.reset(1)
        self.assertEqual(obs.shape[0], env.obs_dim)
        obs2, reward, done, info = env.step(0)
        self.assertEqual(obs2.shape[0], env.obs_dim)
        self.assertIsInstance(reward, float)
        self.assertIn("win", info)


if __name__ == "__main__":
    unittest.main()
