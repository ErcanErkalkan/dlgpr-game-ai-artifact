"""Policy and representation utilities."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class LinearSoftmaxPolicy:
    obs_dim: int
    action_dim: int
    temperature: float = 1.0

    @property
    def param_dim(self) -> int:
        return self.obs_dim * self.action_dim

    def zeros(self) -> np.ndarray:
        return np.zeros(self.param_dim, dtype=np.float64)

    def decode(self, theta: np.ndarray) -> np.ndarray:
        theta = np.asarray(theta, dtype=np.float64)
        if theta.size != self.param_dim:
            raise ValueError(f"theta has size {theta.size}, expected {self.param_dim}")
        return theta.reshape(self.obs_dim, self.action_dim)

    def logits(self, theta: np.ndarray, obs: np.ndarray) -> np.ndarray:
        W = self.decode(theta)
        return np.asarray(obs, dtype=np.float64) @ W

    def probs(self, theta: np.ndarray, obs: np.ndarray) -> np.ndarray:
        z = self.logits(theta, obs) / max(1e-9, self.temperature)
        z = z - np.max(z)
        exp = np.exp(z)
        return exp / np.sum(exp)

    def act(self, theta: np.ndarray, obs: np.ndarray, rng: np.random.Generator, deterministic: bool = False) -> int:
        p = self.probs(theta, obs)
        if deterministic:
            return int(np.argmax(p))
        return int(rng.choice(self.action_dim, p=p))

    def behavioral_descriptor(self, theta: np.ndarray) -> np.ndarray:
        """A compact descriptor for diversity instrumentation.

        Uses action probabilities on a fixed synthetic observation grid so that
        diversity is defined even without external benchmark features.
        """
        basis = np.eye(self.obs_dim)
        probs = [self.probs(theta, row) for row in basis]
        return np.concatenate(probs)


def repair_theta(theta: np.ndarray, bound: float = 5.0) -> np.ndarray:
    return np.clip(np.asarray(theta, dtype=np.float64), -bound, bound)
