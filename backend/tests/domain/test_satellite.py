from uuid import UUID

import pytest

from backend.app.domain.satellite import Satellite


def test_satellite_requires_a_name() -> None:
    with pytest.raises(ValueError, match="name"):
        Satellite(name="")


def test_satellite_has_canonical_identity() -> None:
    satellite = Satellite(
        name="IS-901",
        orbit_type="GEO",
        status="operational",
    )

    assert isinstance(satellite.id, UUID)
    assert satellite.name == "IS-901"
    assert satellite.normalized_name == "is-901"


def test_satellite_normalizes_name() -> None:
    satellite = Satellite(
        name="  IS-901  ",
        orbit_type="GEO",
        status="operational",
    )

    assert satellite.name == "IS-901"
    assert satellite.normalized_name == "is-901"


def test_satellite_rejects_non_string_name() -> None:
    with pytest.raises(TypeError, match="name"):
        Satellite(
            name=None,
            orbit_type="GEO",
            status="operational",
        )


def test_satellite_accepts_supported_orbit_type() -> None:
    satellite = Satellite(
        name="IS-901",
        orbit_type="GEO",
        status="operational",
    )

    assert satellite.orbit_type == "GEO"


def test_satellite_rejects_unsupported_orbit_type() -> None:
    with pytest.raises(ValueError, match="orbit_type"):
        Satellite(
            name="IS-901",
            orbit_type="MOON",
            status="operational",
        )


def test_satellite_accepts_supported_status() -> None:
    satellite = Satellite(
        name="IS-901",
        orbit_type="GEO",
        status="operational",
    )

    assert satellite.status == "operational"


def test_satellite_rejects_unsupported_status() -> None:
    with pytest.raises(ValueError, match="status"):
        Satellite(
            name="IS-901",
            orbit_type="GEO",
            status="banana",
        )


def test_satellites_with_same_normalized_name_are_equal() -> None:
    first = Satellite(
        name="IS-901",
        orbit_type="GEO",
        status="operational",
    )
    second = Satellite(
        name=" is-901 ",
        orbit_type="GEO",
        status="operational",
    )

    assert first == second


def test_satellites_with_different_normalized_names_are_not_equal() -> None:
    first = Satellite(
        name="IS-901",
        orbit_type="GEO",
        status="operational",
    )
    second = Satellite(
        name="IS-902",
        orbit_type="GEO",
        status="operational",
    )

    assert first != second


def test_satellite_can_be_compared_with_non_satellite() -> None:
    satellite = Satellite(
        name="IS-901",
        orbit_type="GEO",
        status="operational",
    )

    assert satellite != "IS-901"
