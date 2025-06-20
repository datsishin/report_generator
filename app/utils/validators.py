import zoneinfo
from datetime import datetime, time
from typing import ClassVar, Self

from pydantic import field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

Number = int | float


class TestMetricsValidatorMixin:
    METRIC_LIMITS: ClassVar[dict[str, tuple[Number, Number]]] = {
        "height": (80, 250),
        "weight": (40, 200),
        "vo2max": (20, 100),
        "vo2max_heart_rate": (40, 240),
        "lt1_heart_rate": (40, 240),
        "lt2_heart_rate": (40, 240),
        "lt1_power": (50, 500),
        "lt2_power": (50, 500),
        "lt1_vo2_usage_percent": (10, 100),
        "lt2_vo2_usage_percent": (10, 100),
        "body_fat_percent": (2, 60),
    }

    @model_validator(mode="after")
    def check_metrics(self) -> Self:
        errors = []
        for field, (min_val, max_val) in self.METRIC_LIMITS.items():
            value = getattr(self, field)
            if not (min_val <= value <= max_val):
                errors.append(f"{field}={value} out of range ({min_val}–{max_val})")

        if errors:
            error_msg = "Invalid metrics:\n" + "\n".join(errors)
            raise ValueError(error_msg)

        return self


class TestInfoValidatorMixin:

    """Миксин для валидации общих данных теста."""

    NAME_LENGTH_LIMITS: ClassVar[dict[str, tuple[int, int]]] = {
        "first_name": (2, 30),
        "last_name": (2, 50),
    }

    @field_validator("first_name", "last_name")
    def validate_name_length(cls, value: str, info: ValidationInfo) -> str:
        min_len, max_len = cls.NAME_LENGTH_LIMITS.get(info.field_name, (2, 50))
        if not (min_len <= len(value) <= max_len):
            error_msg = f"{info.field_name} must be between {min_len} and {max_len} characters long"
            raise ValueError(error_msg)
        return value

    MIN_AGE: ClassVar[int] = 1
    MAX_AGE: ClassVar[int] = 100
    TIMEZONE: ClassVar[str] = "Europe/Moscow"

    @model_validator(mode="after")
    def validate_age_and_date(self) -> Self:
        if not (self.MIN_AGE <= self.age <= self.MAX_AGE):
            error_msg = f"Age must be between {self.MIN_AGE} and {self.MAX_AGE}"
            raise ValueError(error_msg)

        if hasattr(self, "test_date"):
            tz = zoneinfo.ZoneInfo(self.TIMEZONE)
            test_datetime = datetime.combine(self.test_date, time.min).replace(tzinfo=tz)
            current_datetime = datetime.now(tz)
            if test_datetime > current_datetime:
                error_msg = "Test date cannot be in the future"
                raise ValueError(error_msg)

        return self


class LactateMeasurementValidatorMixin:
    METRIC_LIMITS: ClassVar[dict[str, tuple[Number, Number]]] = {
        "step": (1, 50),
        "time": (60, 50 * 180),  # 50 ступеней по 3 минуты
        "intensity": (1, 1000),
        "heart_rate": (30, 240),
        "lactate": (0.1, 50),
    }

    @model_validator(mode="after")
    def check_metrics(self) -> Self:
        errors = []
        for field, (min_val, max_val) in self.METRIC_LIMITS.items():
            value = getattr(self, field)
            if not (min_val <= value <= max_val):
                errors.append(f"{field}={value} out of range ({min_val}–{max_val})")

        if errors:
            error_msg = "Invalid metrics:\n" + "\n".join(errors)
            raise ValueError(error_msg)

        return self
