"""Analysis metrics with dependency-light statistical fallbacks."""
from __future__ import annotations

from math import comb
from typing import Iterable, List, Tuple
import numpy as np


def _finite_array(x: Iterable[float]) -> np.ndarray:
    arr = np.asarray(list(x), dtype=np.float64)
    return arr[np.isfinite(arr)]


def _paired_differences(x: Iterable[float], y: Iterable[float]) -> np.ndarray:
    a = np.asarray(list(x), dtype=np.float64)
    b = np.asarray(list(y), dtype=np.float64)
    n = min(a.size, b.size)
    if n == 0:
        return np.asarray([], dtype=np.float64)
    d = a[:n] - b[:n]
    return d[np.isfinite(d)]


def _t_critical_95(n: int) -> float:
    """Return the two-sided 95% Student-t critical value.

    SciPy is used when installed. The small lookup table keeps the analysis
    reproducible in dependency-light review environments.
    """
    if n <= 1:
        return 0.0
    try:
        from scipy.stats import t  # type: ignore
        return float(t.ppf(0.975, df=n - 1))
    except Exception:
        table = {
            1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
            6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
            11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
            16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
            21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
            26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042,
        }
        return table.get(n - 1, 1.96)


def mean_std_ci(x: Iterable[float]) -> Tuple[float, float, float]:
    """Return mean, sample standard deviation, and Student-t 95% half-width."""
    arr = _finite_array(x)
    if arr.size == 0:
        return float("nan"), float("nan"), float("nan")
    mean = float(np.mean(arr))
    std = float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0
    ci = float(_t_critical_95(arr.size) * std / np.sqrt(arr.size)) if arr.size > 1 else 0.0
    return mean, std, ci


def paired_cohens_dz(x: Iterable[float], y: Iterable[float]) -> float:
    """Return paired Cohen's dz for x - y; positive values favor x."""
    d = _paired_differences(x, y)
    if d.size == 0:
        return float("nan")
    if d.size == 1:
        return 0.0 if np.isclose(d[0], 0.0) else float("nan")
    std = float(np.std(d, ddof=1))
    if np.isclose(std, 0.0):
        return 0.0 if np.isclose(np.mean(d), 0.0) else float(np.sign(np.mean(d)) * np.inf)
    return float(np.mean(d) / std)


def paired_rank_biserial(x: Iterable[float], y: Iterable[float]) -> float:
    """Return matched-pairs rank-biserial correlation for x - y.

    Ties are removed, matching the Wilcoxon signed-rank convention. Positive
    values favor x and negative values favor y.
    """
    d = _paired_differences(x, y)
    d = d[~np.isclose(d, 0.0)]
    if d.size == 0:
        return 0.0
    try:
        from scipy.stats import rankdata  # type: ignore
        ranks = np.asarray(rankdata(np.abs(d), method="average"), dtype=np.float64)
    except Exception:
        order = np.argsort(np.abs(d), kind="mergesort")
        ranks = np.empty(d.size, dtype=np.float64)
        sorted_abs = np.abs(d)[order]
        start = 0
        while start < d.size:
            end = start + 1
            while end < d.size and np.isclose(sorted_abs[end], sorted_abs[start]):
                end += 1
            ranks[order[start:end]] = (start + 1 + end) / 2.0
            start = end
    positive = float(np.sum(ranks[d > 0]))
    negative = float(np.sum(ranks[d < 0]))
    return float((positive - negative) / max(positive + negative, 1e-12))


def paired_mean_difference_ci(
    x: Iterable[float], y: Iterable[float], *, n_bootstrap: int = 10000, seed: int = 20260601
) -> Tuple[float, float, float]:
    """Return paired mean difference and deterministic bootstrap percentile CI."""
    d = _paired_differences(x, y)
    if d.size == 0:
        return float("nan"), float("nan"), float("nan")
    mean = float(np.mean(d))
    if d.size == 1 or np.allclose(d, d[0]):
        return mean, mean, mean
    rng = np.random.default_rng(seed)
    samples = rng.choice(d, size=(int(n_bootstrap), d.size), replace=True)
    boot_means = np.mean(samples, axis=1)
    low, high = np.percentile(boot_means, [2.5, 97.5])
    return mean, float(low), float(high)


def paired_sign_test_p_value(x: Iterable[float], y: Iterable[float]) -> float:
    """Two-sided exact sign test for paired samples.

    This is used as a dependency-free fallback when scipy/Wilcoxon is unavailable.
    """
    a = np.asarray(list(x), dtype=np.float64)
    b = np.asarray(list(y), dtype=np.float64)
    n = min(a.size, b.size)
    if n == 0:
        return float("nan")
    d = a[:n] - b[:n]
    d = d[d != 0]
    n = d.size
    if n == 0:
        return 1.0
    k = int(min(np.sum(d > 0), np.sum(d < 0)))
    prob = 2.0 * sum(comb(n, i) for i in range(k + 1)) / (2 ** n)
    return float(min(1.0, prob))



def paired_wilcoxon_p_value(x: Iterable[float], y: Iterable[float]) -> Tuple[float, str]:
    """Two-sided paired Wilcoxon p-value with dependency-free fallback.

    Returns (p_value, test_name). SciPy is used when available; otherwise the
    exact sign-test fallback is returned.
    """
    a = np.asarray(list(x), dtype=np.float64)
    b = np.asarray(list(y), dtype=np.float64)
    n = min(a.size, b.size)
    if n == 0:
        return float("nan"), "unavailable"
    a = a[:n]
    b = b[:n]
    if np.allclose(a, b):
        return 1.0, "paired Wilcoxon signed-rank (all ties)"
    try:
        from scipy.stats import wilcoxon  # type: ignore
        stat = wilcoxon(a, b, zero_method="wilcox", alternative="two-sided", method="auto")
        p = float(stat.pvalue)
        if not np.isfinite(p):
            return paired_sign_test_p_value(a, b), "paired exact sign test fallback"
        return p, "paired Wilcoxon signed-rank"
    except Exception:
        return paired_sign_test_p_value(a, b), "paired exact sign test fallback"


def holm_bonferroni(p_values: Iterable[float]) -> List[float]:
    """Return Holm-Bonferroni adjusted p-values in the input order."""
    arr = np.asarray(list(p_values), dtype=np.float64)
    adjusted = np.full(arr.shape, np.nan, dtype=np.float64)
    finite_idx = np.where(np.isfinite(arr))[0]
    m = finite_idx.size
    if m == 0:
        return adjusted.tolist()
    ordered = finite_idx[np.argsort(arr[finite_idx])]
    prev = 0.0
    for rank, idx in enumerate(ordered):
        raw = float((m - rank) * arr[idx])
        prev = max(prev, raw)
        adjusted[idx] = min(1.0, prev)
    return adjusted.tolist()
