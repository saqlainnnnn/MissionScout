from uuid import uuid4

from backend.app.domain.operator import Operator
from backend.app.mappers.operator import OperatorMapper
from backend.app.models.operator import OperatorModel


def test_domain_to_model() -> None:
    operator_id = uuid4()

    operator = Operator(
        name="  Example Space Systems  ",
        country="India",
    )
    operator.id = operator_id

    model = OperatorMapper.to_model(operator)

    assert model.id == operator_id
    assert model.name == "Example Space Systems"
    assert model.normalized_name == "example space systems"
    assert model.country == "India"


def test_model_to_domain() -> None:
    operator_id = uuid4()

    model = OperatorModel(
        id=operator_id,
        name="Example Space Systems",
        normalized_name="example space systems",
        country="India",
    )

    operator = OperatorMapper.to_domain(model)

    assert operator.id == operator_id
    assert operator.name == "Example Space Systems"
    assert operator.normalized_name == "example space systems"
    assert operator.country == "India"
