"""Analysis metrics without heavy statistical dependencies."""
from __future__ import annotations

from math import comb
from typing import Iterable, Tuple
import numpy as np


def mean_std_ci(x: Iterable[float]) -> Tuple[float, float, float]:
    arr = np.asarray(list(x), dtype=np.float64)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan"), float("nan"), float("nan")
    mean = float(np.mean(arr))
    std = float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0
    ci = float(1.96 * std / np.sqrt(arr.size)) if arr.size > 1 else 0.0
    return mean, std, ci


def cliffs_delta(x: Iterable[float], y: Iterable[float]) -> float:
    a = np.asarray(list(x), dtype=np.float64)
    b = np.asarray(list(y), dtype=np.float64)
    if a.size == 0 or b.size == 0:
        return float("nan")
    greater = 0
    less = 0
    for ai in a:
        greater += int(np.sum(ai > b))
        less += int(np.sum(ai < b))
    return float((greater - less) / (a.size * b.size))


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
