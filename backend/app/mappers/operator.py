from backend.app.domain.operator import Operator
from backend.app.models.operator import OperatorModel


class OperatorMapper:
    @staticmethod
    def to_model(operator: Operator) -> OperatorModel:
        return OperatorModel(
            id=operator.id,
            name=operator.name,
            normalized_name=operator.normalized_name,
            country=operator.country,
        )

    @staticmethod
    def to_domain(model: OperatorModel) -> Operator:
        operator = Operator(
            name=model.name,
            country=model.country,
        )
        operator.id = model.id
        return operator
