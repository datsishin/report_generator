import json

from fastapi import FastAPI
from pydantic import ValidationError

from app.api.routes import router
from app.exceptions.handlers import (
    general_exception_handler,
    json_decode_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title="Report generate service",
    description="Сервис для генерации отчётов о тестировании",
    version="0.1.0",
)

app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(json.JSONDecodeError, json_decode_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(router, prefix="/api/v1")
