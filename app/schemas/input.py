import datetime
import zoneinfo
from datetime import date
from typing import Self

from pydantic import BaseModel, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from app.schemas.enums import TestType

Number = int | float

TZ = zoneinfo.ZoneInfo("Europe/Moscow")
MIN_AGE = 1
MAX_AGE = 100
NAME_LENGTH_LIMITS = {
    "first_name": (2, 30),
    "last_name": (2, 50),
}


class TestInfo(BaseModel):
    first_name: str
    last_name: str
    test_type: TestType
    test_date: date
    age: int

    @field_validator("first_name", "last_name")
    def name_must_be_long_enough(cls, value: str, info: ValidationInfo) -> str:  # noqa: N805
        """
        Валидация длины имени и фамилии по длине.

        Args:
            value (str): Значение поля (имя или фамилия).
            info (ValidationInfo): Информация о поле.

        Returns:
            str: Проверенное значение.

        Raises:
            ValueError: Если длина имени или фамилии не в допустимом диапазоне.

        """
        min_len, max_len = NAME_LENGTH_LIMITS.get(info.field_name, (2, 50))
        if not (min_len <= len(value) <= max_len):
            error_msg = f"{info.field_name} must be at least 2 characters long"
            raise ValueError(error_msg)
        return value

    @model_validator(mode="after")
    def check_age_and_test_date(self) -> Self:

        if self.age <= MIN_AGE or self.age > MAX_AGE:
            error_msg = f"age must be between {MIN_AGE} and {MAX_AGE}"
            raise ValueError(error_msg)

        if self.test_date > datetime.datetime.now(tz=TZ):
            error_msg = "date of test cannot be in the future"
            raise ValueError(error_msg)
        return self


class TestMetrics(BaseModel):
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

    @model_validator(mode="after")
    def check_athlete_metrics(self) -> Self:
        limits = {
            "height": (100, 250),
            "weight": (40, 200),
            "vo2max": (20, 100),
            "vo2max_heart_rate": (80, 240),
            "lt1_heart_rate": (60, 220),
            "lt2_heart_rate": (60, 220),
            "lt1_power": (50, 500),
            "lt2_power": (50, 500),
            "lt1_vo2_usage_percent": (10, 100),
            "lt2_vo2_usage_percent": (10, 100),
            "body_fat_percent": (2, 60),
        }

        errors = []
        for field, (min_val, max_val) in limits.items():
            value = getattr(self, field)
            if not (min_val <= value <= max_val):
                errors.append(f"{field}={value} out of range ({min_val}–{max_val})")

        if errors:
            error_msg = "Invalid metrics:\n" + "\n".join(errors)
            raise ValueError(error_msg)

        return self


class TestInput(TestInfo, TestMetrics):
    pass
