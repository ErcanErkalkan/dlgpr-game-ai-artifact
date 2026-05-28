# External Benchmark Adapter Guide

The package includes self-contained local environments for reproducibility and smoke validation. These environments fix the metadata problem but are not a substitute for recognized Game AI benchmarks.

For journal-strength evidence, connect at least two or three external benchmarks, for example:

- GVGAI-style game tasks,
- MicroRTS maps/opponents,
- Procgen-style generalization tasks,
- Gymnasium-compatible discrete-action tasks as preliminary adapters.

## Required adapter contract

An adapter must expose:

```python
obs_dim: int
action_dim: int
metadata: EnvMetadata
reset(seed: int | None) -> np.ndarray
step(action: int) -> tuple[np.ndarray, float, bool, dict]
clone(seed: int | None) -> BaseGameEnv
```

The `EnvMetadata` object must define the environment name/version, observation and action definitions, reward, termination, opponent policy, stochasticity sources, and max steps.

## Provided code

`dlgpr.external_adapters.GymnasiumDiscreteAdapter` provides a minimal wrapper for vector-observation, discrete-action Gymnasium-style environments. It is optional and not required for the self-contained tests.

## Manuscript rule

Do not claim cross-benchmark Game AI generalization using only the self-contained environments. Use them as reproducibility and implementation evidence only.
