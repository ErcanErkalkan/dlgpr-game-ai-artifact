# External Benchmark Adapter Guide

The package includes self-contained local environments for reproducibility and smoke validation. These environments fix the metadata problem but are not a substitute for recognized Game AI benchmarks.

For journal-strength evidence, connect at least two or three external benchmarks, for example:

- GVGAI-style game tasks,
- MicroRTS maps/opponents,
- Procgen-style generalization tasks,
- Gymnasium-compatible discrete-action tasks as preliminary adapters.
- MiniGrid tasks through the Gymnasium adapter when dictionary observations can be flattened.

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

`dlgpr.external_adapters.GymnasiumDiscreteAdapter` provides a wrapper for discrete-action Gymnasium-style environments. It supports discrete observations, vector observations, and numeric dictionary observations such as MiniGrid image/direction dictionaries.

The release includes completed logs for these default external tasks:

- `gym-frozenlake-4x4`
- `gym-frozenlake-4x4-deterministic`
- `gym-cliffwalking`
- `gym-blackjack`

The release also includes an optional MiniGrid adapter:

- `minigrid-empty-5x5`

MiniGrid is included in the raw-CPU timing profile, but not in the default external performance run. The simple linear policy is not a strong MiniGrid controller, so MiniGrid results must be treated as adapter and timing diagnostics unless a stronger policy class is added.

## Manuscript rule

Do not claim cross-benchmark Game AI generalization using only the self-contained environments. The Gymnasium extension supports only the named tasks that were logged. It still does not justify claims about GVGAI, MicroRTS, Procgen, or OpenSpiel unless those benchmarks are connected and logged with the same metadata fields.
