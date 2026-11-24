"""Closed-form epidemic quantities for the SEIR model.

These hold for a well-mixed population with exponentially distributed latent and infectious
periods. They are the checks the simulator is held to: a large, well-mixed town must grow
at the rate and reach the final size these formulas predict.
"""

from __future__ import annotations

import math


def _check_periods(latent_days: float, infectious_days: float) -> None:
    if latent_days < 0:
        raise ValueError("latent period cannot be negative")
    if infectious_days <= 0:
        raise ValueError("infectious period must be positive")


def r0_from_growth_rate(growth_per_day: float, latent_days: float, infectious_days: float) -> float:
    """Return R0 for an early exponential growth rate: R0 = (1 + r L)(1 + r D)."""
    _check_periods(latent_days, infectious_days)
    latent_factor = 1.0 + growth_per_day * latent_days
    infectious_factor = 1.0 + growth_per_day * infectious_days
    if latent_factor <= 0 or infectious_factor <= 0:
        raise ValueError("decline is faster than the model allows")
    return latent_factor * infectious_factor


def growth_rate_from_r0(r0: float, latent_days: float, infectious_days: float) -> float:
    """Return the early exponential growth rate per day for a given R0."""
    _check_periods(latent_days, infectious_days)
    if r0 <= 0:
        raise ValueError("R0 must be positive")
    # Positive root of L D r^2 + (L + D) r + (1 - R0) = 0, in the form that avoids
    # cancellation when L D is small (and reduces to (R0 - 1) / D when L = 0).
    a = latent_days * infectious_days
    b = latent_days + infectious_days
    return 2.0 * (r0 - 1.0) / (b + math.sqrt(b * b + 4.0 * a * (r0 - 1.0)))


def doubling_time_days(growth_per_day: float) -> float:
    if growth_per_day <= 0:
        raise ValueError("an epidemic that is not growing has no doubling time")
    return math.log(2.0) / growth_per_day


def final_size(r0: float, tolerance: float = 1e-12) -> float:
    """Return the fraction of a fully susceptible population ever infected.

    Solves z = 1 - exp(-R0 z) for its positive root; below R0 = 1 the answer is 0.
    """
    if r0 < 0:
        raise ValueError("R0 cannot be negative")
    if r0 <= 1.0:
        return 0.0
    lo, hi = 1e-15, 1.0
    while hi - lo > tolerance:
        mid = (lo + hi) / 2.0
        if mid - (1.0 - math.exp(-r0 * mid)) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def herd_immunity_threshold(r0: float) -> float:
    """Return the immune fraction above which an outbreak cannot grow: 1 - 1/R0."""
    if r0 <= 0:
        raise ValueError("R0 must be positive")
    return max(0.0, 1.0 - 1.0 / r0)
