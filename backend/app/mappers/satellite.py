from uuid import UUID

from backend.app.domain.satellite import Satellite
from backend.app.models.satellite import SatelliteModel


class SatelliteMapper:
    @staticmethod
    def to_model(
        satellite: Satellite,
        *,
        operator_id: UUID,
    ) -> SatelliteModel:
        return SatelliteModel(
            id=satellite.id,
            operator_id=operator_id,
            name=satellite.name,
            normalized_name=satellite.normalized_name,
            orbit_type=satellite.orbit_type,
            status=satellite.status,
        )

    @staticmethod
    def to_domain(
        model: SatelliteModel,
    ) -> Satellite:
        satellite = Satellite(
            name=model.name,
            orbit_type=model.orbit_type,
            status=model.status,
        )
        satellite.id = model.id
        return satellite
