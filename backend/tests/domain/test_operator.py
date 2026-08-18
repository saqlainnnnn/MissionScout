from uuid import UUID

import pytest

from backend.app.domain.operator import Operator


def test_operator_requires_a_name() -> None:
    with pytest.raises(ValueError, match="name"):
        Operator(name="")


def test_operator_has_canonical_identity() -> None:
    operator = Operator(name="Example Space Systems")

    assert isinstance(operator.id, UUID)
    assert operator.name == "Example Space Systems"


def test_operator_normalizes_surrounding_whitespace() -> None:
    operator = Operator(name="  Example Space Systems  ")

    assert operator.name == "Example Space Systems"


def test_operator_preserves_country_when_provided() -> None:
    operator = Operator(
        name="Example Space Systems",
        country="India",
    )

    assert operator.country == "India"


def test_operator_name_comparison_is_case_insensitive() -> None:
    first = Operator(name="Example Space Systems")
    second = Operator(name="example space systems")

    assert first.normalized_name == second.normalized_name


def test_operator_exposes_normalized_name() -> None:
    operator = Operator(name="  Example SPACE Systems  ")

    assert operator.normalized_name == "example space systems"


def test_operator_rejects_non_string_name() -> None:
    with pytest.raises(TypeError, match="name"):
        Operator(name=None)


def test_operators_with_same_normalized_name_are_equal() -> None:
    first = Operator(name="Example Space Systems")
    second = Operator(name=" example space systems ")

    assert first == second


def test_operators_with_different_normalized_names_are_not_equal() -> None:
    first = Operator(name="Example Space Systems")
    second = Operator(name="Another Space Systems")

    assert first != second


def test_operator_can_be_compared_with_non_operator() -> None:
    operator = Operator(name="Example Space Systems")

    assert operator != "Example Space Systems"


def test_operator_starts_with_no_satellites() -> None:
    operator = Operator(name="Example Space Systems")

    assert operator.satellites == []


def test_operator_can_add_satellite() -> None:
    from backend.app.domain.satellite import Satellite

    operator = Operator(name="Example Space Systems")
    satellite = Satellite(
        name="IS-901",
        orbit_type="GEO",
        status="operational",
    )

    operator.add_satellite(satellite)

    assert operator.satellites == [satellite]


def test_operator_rejects_duplicate_satellite() -> None:
    from backend.app.domain.satellite import Satellite

    operator = Operator(name="Example Space Systems")
    satellite = Satellite(
        name="IS-901",
        orbit_type="GEO",
        status="operational",
    )

    operator.add_satellite(satellite)
    operator.add_satellite(satellite)

    assert operator.satellites == [satellite]


def test_operator_rejects_non_satellite() -> None:
    operator = Operator(name="Example Space Systems")

    with pytest.raises(TypeError, match="satellite"):
        operator.add_satellite("IS-901")
