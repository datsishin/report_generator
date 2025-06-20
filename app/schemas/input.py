from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.schemas.enums import TestType
from app.utils.validators import (
    LactateMeasurementValidatorMixin,
    TestInfoValidatorMixin,
    TestMetricsValidatorMixin,
)

Number = int | float


class TestInfo(BaseModel, TestInfoValidatorMixin):
    model_config = ConfigDict(
        alias_generator=to_camel,  # для генерации алиасов в camelCase
        populate_by_name=True,  # разрешить использовать как camelCase, так и snake_case
    )

    first_name: str
    last_name: str
    test_type: TestType
    test_date: date
    age: int


class LactateMeasurement(BaseModel, LactateMeasurementValidatorMixin):
    model_config = ConfigDict(
        alias_generator=to_camel,  # для генерации алиасов в camelCase
        populate_by_name=True,  # разрешить использовать как camelCase, так и snake_case
    )

    step: int
    time: int
    intensity: int
    heart_rate: int
    lactate: Number


class TestMetrics(BaseModel, TestMetricsValidatorMixin):
    height: Number
    weight: Number
    vo2max: Number
    vo2max_heart_rate: int
    lt1_heart_rate: int
    lt1_power: Number
    lt2_heart_rate: int
    lt2_power: Number
    lt1_vo2_usage_percent: Number
    lt2_vo2_usage_percent: Number
    body_fat_percent: Number
    starting_level: int
    step_duration: int
    step_amplitude: int
    number_of_steps: int
    lactate_data: list[LactateMeasurement]


class TestInput(TestInfo, TestMetrics):
    pass
