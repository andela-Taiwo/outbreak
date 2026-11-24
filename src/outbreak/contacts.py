"""Age-structured contact matrices and the R0 they imply.

``contacts[i][j]`` is the average number of daily contacts a person in group ``i`` has with
people in group ``j``. Survey matrices are rarely reciprocal (the total contacts from group
``i`` to ``j`` should equal those from ``j`` to ``i``), so they are corrected before use.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _validate(
    contacts: ArrayLike, population: ArrayLike
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    c = np.asarray(contacts, dtype=np.float64)
    n = np.asarray(population, dtype=np.float64)
    if c.ndim != 2 or c.shape[0] != c.shape[1]:
        raise ValueError("contact matrix must be square")
    if n.shape != (c.shape[0],):
        raise ValueError("population must have one entry per group")
    if (c < 0).any() or not np.isfinite(c).all():
        raise ValueError("contacts must be finite and non-negative")
    if (n <= 0).any():
        raise ValueError("every group must have a positive population")
    return c, n


def is_reciprocal(contacts: ArrayLike, population: ArrayLike, rtol: float = 1e-9) -> bool:
    """Return whether total contacts between each pair of groups agree both ways."""
    c, n = _validate(contacts, population)
    totals = c * n[:, None]
    return bool(np.allclose(totals, totals.T, rtol=rtol, atol=0))


def make_reciprocal(contacts: ArrayLike, population: ArrayLike) -> NDArray[np.float64]:
    """Average the two directions of each pair so the matrix is reciprocal."""
    c, n = _validate(contacts, population)
    totals = c * n[:, None]
    symmetric = (totals + totals.T) / 2.0
    result: NDArray[np.float64] = symmetric / n[:, None]
    return result


def next_generation_r0(
    contacts: ArrayLike,
    population: ArrayLike,
    transmission_per_contact: float,
    infectious_days: float,
    susceptibility: ArrayLike | None = None,
) -> float:
    """Return R0 as the dominant eigenvalue of the next-generation matrix.

    ``K[i][j]`` is the expected number of infections in group ``i`` caused by one infectious
    person in group ``j``.
    """
    c, n = _validate(contacts, population)
    if not 0 <= transmission_per_contact <= 1:
        raise ValueError("transmission per contact must be a probability")
    if infectious_days <= 0:
        raise ValueError("infectious period must be positive")
    s = np.ones_like(n) if susceptibility is None else np.asarray(susceptibility, dtype=np.float64)
    if s.shape != n.shape or (s < 0).any():
        raise ValueError("susceptibility must be non-negative with one entry per group")
    k = transmission_per_contact * infectious_days * s[:, None] * c.T
    return float(np.max(np.abs(np.linalg.eigvals(k))))
