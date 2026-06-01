# Environment and Task Disclosure Requirements

Every experiment must disclose:

- environment name and version,
- task/game/map name,
- observation definition,
- action definition,
- reward definition,
- episode termination,
- opponent policy,
- stochasticity sources,
- training seed schedule,
- evaluation seed schedule,
- evaluation cadence,
- rollout horizon H,
- number of rollouts K,
- budget unit and rollout-equivalent charge when normalized compute accounting is used,
- performance threshold T if Steps-to-T is reported,
- hardware and runtime,
- OS and library versions,
- B_tau, loop budget, delta_min, delta_max, guard margin,
- environment-step cap.

If any field is missing, the run may be used for debugging but not for manuscript performance claims.
