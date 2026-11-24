import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays

from outbreak.contacts import is_reciprocal, make_reciprocal, next_generation_r0

CHILDREN_ADULTS = [[8.0, 4.0], [1.0, 6.0]]
POPULATION = [200.0, 800.0]


def test_survey_matrix_is_detected_as_not_reciprocal() -> None:
    # 200 * 4 = 800 child-adult contacts, but 800 * 1 = 800 adult-child: this one agrees.
    assert is_reciprocal(CHILDREN_ADULTS, POPULATION)
    assert not is_reciprocal([[8.0, 5.0], [1.0, 6.0]], POPULATION)


def test_make_reciprocal_by_hand() -> None:
    fixed = make_reciprocal([[8.0, 5.0], [1.0, 6.0]], POPULATION)
    # totals: 200*5 = 1000 and 800*1 = 800 -> 900 each way
    assert fixed == pytest.approx(np.array([[8.0, 4.5], [1.125, 6.0]]))


@given(
    arrays(np.float64, (3, 3), elements=st.floats(0, 30)),
    arrays(np.float64, (3,), elements=st.floats(1, 1e6)),
)
def test_make_reciprocal_always_gives_a_reciprocal_matrix(
    contacts: np.ndarray, population: np.ndarray
) -> None:
    assert is_reciprocal(make_reciprocal(contacts, population), population, rtol=1e-7)


def test_one_group_r0_is_contacts_times_transmission_times_duration() -> None:
    assert next_generation_r0([[10.0]], [1000.0], 0.05, 4) == pytest.approx(2.0)


def test_uniform_groups_behave_like_one_group() -> None:
    contacts = [[5.0, 5.0], [5.0, 5.0]]
    assert next_generation_r0(contacts, [500.0, 500.0], 0.05, 4) == pytest.approx(2.0)


def test_lower_susceptibility_lowers_r0() -> None:
    full = next_generation_r0(CHILDREN_ADULTS, POPULATION, 0.05, 4)
    reduced = next_generation_r0(CHILDREN_ADULTS, POPULATION, 0.05, 4, susceptibility=[0.5, 1])
    assert reduced < full


def test_r0_scales_linearly_with_transmission() -> None:
    a = next_generation_r0(CHILDREN_ADULTS, POPULATION, 0.02, 4)
    b = next_generation_r0(CHILDREN_ADULTS, POPULATION, 0.04, 4)
    assert b == pytest.approx(2 * a)


@pytest.mark.parametrize(
    ("contacts", "population"),
    [
        ([[1.0, 2.0]], [1.0]),
        ([[1.0]], [1.0, 2.0]),
        ([[-1.0]], [1.0]),
        ([[1.0]], [0.0]),
        ([[float("nan")]], [1.0]),
    ],
)
def test_bad_inputs_are_rejected(contacts: list[list[float]], population: list[float]) -> None:
    with pytest.raises(ValueError):
        make_reciprocal(contacts, population)


def test_bad_transmission_is_rejected() -> None:
    with pytest.raises(ValueError):
        next_generation_r0([[1.0]], [1.0], 1.5, 4)
