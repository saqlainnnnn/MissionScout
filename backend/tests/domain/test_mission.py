from uuid import UUID

import pytest

from backend.app.domain.mission import Mission


def test_mission_requires_a_name() -> None:
    with pytest.raises(ValueError, match="name"):
        Mission(name="")


def test_mission_has_canonical_identity() -> None:
    mission = Mission(
        name="Primary Communications Mission",
        mission_type="communications",
        status="active",
    )

    assert isinstance(mission.id, UUID)
    assert mission.name == "Primary Communications Mission"
    assert mission.normalized_name == "primary communications mission"


def test_mission_normalizes_name() -> None:
    mission = Mission(
        name="  Primary COMMUNICATIONS Mission  ",
        mission_type="communications",
        status="active",
    )

    assert mission.name == "Primary COMMUNICATIONS Mission"
    assert mission.normalized_name == "primary communications mission"


def test_mission_rejects_non_string_name() -> None:
    with pytest.raises(TypeError, match="name"):
        Mission(
            name=None,
            mission_type="communications",
            status="active",
        )


def test_mission_accepts_supported_mission_type() -> None:
    mission = Mission(
        name="Primary Communications Mission",
        mission_type="communications",
        status="active",
    )

    assert mission.mission_type == "communications"


def test_mission_rejects_unsupported_mission_type() -> None:
    with pytest.raises(ValueError, match="mission_type"):
        Mission(
            name="Primary Communications Mission",
            mission_type="banana",
            status="active",
        )


def test_mission_accepts_supported_status() -> None:
    mission = Mission(
        name="Primary Communications Mission",
        mission_type="communications",
        status="active",
    )

    assert mission.status == "active"


def test_mission_rejects_unsupported_status() -> None:
    with pytest.raises(ValueError, match="status"):
        Mission(
            name="Primary Communications Mission",
            mission_type="communications",
            status="banana",
        )


def test_missions_with_same_normalized_name_are_equal() -> None:
    first = Mission(
        name="Primary Communications Mission",
        mission_type="communications",
        status="active",
    )
    second = Mission(
        name=" primary communications mission ",
        mission_type="communications",
        status="active",
    )

    assert first == second


def test_missions_with_different_normalized_names_are_not_equal() -> None:
    first = Mission(
        name="Primary Communications Mission",
        mission_type="communications",
        status="active",
    )
    second = Mission(
        name="Secondary Communications Mission",
        mission_type="communications",
        status="active",
    )

    assert first != second


def test_mission_can_be_compared_with_non_mission() -> None:
    mission = Mission(
        name="Primary Communications Mission",
        mission_type="communications",
        status="active",
    )

    assert mission != "Primary Communications Mission"
