import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from outbreak.epi import (
    doubling_time_days,
    final_size,
    growth_rate_from_r0,
    herd_immunity_threshold,
    r0_from_growth_rate,
)


def test_r0_from_growth_rate_by_hand() -> None:
    # r = 0.1/day, L = 3, D = 5 -> 1.3 * 1.5
    assert r0_from_growth_rate(0.1, 3, 5) == pytest.approx(1.95)


def test_no_growth_means_r0_of_one() -> None:
    assert r0_from_growth_rate(0, 3, 5) == 1.0
    assert growth_rate_from_r0(1.0, 3, 5) == pytest.approx(0.0, abs=1e-15)


def test_sir_case_without_latent_period() -> None:
    assert growth_rate_from_r0(3.0, 0, 5) == pytest.approx(0.4)


@given(st.floats(0.2, 15), st.floats(0, 14), st.floats(0.5, 21))
def test_growth_and_r0_round_trip(r0: float, latent: float, infectious: float) -> None:
    r = growth_rate_from_r0(r0, latent, infectious)
    assert r0_from_growth_rate(r, latent, infectious) == pytest.approx(r0, rel=1e-9)


@pytest.mark.parametrize(("latent", "infectious"), [(-1, 5), (3, 0)])
def test_bad_periods_are_rejected(latent: float, infectious: float) -> None:
    with pytest.raises(ValueError):
        growth_rate_from_r0(2, latent, infectious)


def test_doubling_time() -> None:
    assert doubling_time_days(math.log(2) / 3) == pytest.approx(3)
    with pytest.raises(ValueError):
        doubling_time_days(0)


@pytest.mark.parametrize(("r0", "expected"), [(1.5, 0.5828), (2.0, 0.7968), (3.0, 0.9405)])
def test_final_size_known_values(r0: float, expected: float) -> None:
    assert final_size(r0) == pytest.approx(expected, abs=1e-4)


@given(st.floats(1.01, 20))
def test_final_size_satisfies_its_equation(r0: float) -> None:
    z = final_size(r0)
    assert 0 < z < 1
    assert z == pytest.approx(1 - math.exp(-r0 * z), abs=1e-10)


def test_no_epidemic_below_threshold() -> None:
    assert final_size(0.9) == 0.0
    assert final_size(1.0) == 0.0


def test_herd_immunity_threshold() -> None:
    assert herd_immunity_threshold(4) == 0.75
    assert herd_immunity_threshold(0.8) == 0.0


def test_final_size_exceeds_herd_immunity_threshold() -> None:
    # Overshoot: an unmitigated epidemic infects more than it needs to stop growing.
    for r0 in (1.2, 2, 5):
        assert final_size(r0) > herd_immunity_threshold(r0)
