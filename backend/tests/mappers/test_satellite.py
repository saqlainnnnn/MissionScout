from uuid import uuid4

from backend.app.domain.satellite import Satellite
from backend.app.mappers.satellite import SatelliteMapper
from backend.app.models.satellite import SatelliteModel


def test_domain_to_model() -> None:
    satellite_id = uuid4()
    operator_id = uuid4()

    satellite = Satellite(
        name="  IS-901  ",
        orbit_type="GEO",
        status="operational",
    )
    satellite.id = satellite_id

    model = SatelliteMapper.to_model(
        satellite,
        operator_id=operator_id,
    )

    assert model.id == satellite_id
    assert model.operator_id == operator_id
    assert model.name == "IS-901"
    assert model.normalized_name == "is-901"
    assert model.orbit_type == "GEO"
    assert model.status == "operational"


def test_model_to_domain() -> None:
    satellite_id = uuid4()
    operator_id = uuid4()

    model = SatelliteModel(
        id=satellite_id,
        operator_id=operator_id,
        name="IS-901",
        normalized_name="is-901",
        orbit_type="GEO",
        status="operational",
    )

    satellite = SatelliteMapper.to_domain(model)

    assert satellite.id == satellite_id
    assert satellite.name == "IS-901"
    assert satellite.normalized_name == "is-901"
    assert satellite.orbit_type == "GEO"
    assert satellite.status == "operational"
