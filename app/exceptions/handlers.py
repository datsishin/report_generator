import json
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


def clean_errors(errors: list[Any]) -> list[dict[str, Any]]:
    cleaned = []
    for err in errors:
        err_dict = dict(err)
        if "ctx" in err_dict:
            ctx = dict(err_dict["ctx"])
            for k, v in ctx.items():
                if isinstance(v, Exception):
                    ctx[k] = str(v)
            err["ctx"] = ctx
        cleaned.append(err)
    return cleaned


async def validation_exception_handler(_request: Request, exc: ValidationError) -> JSONResponse:
    errors = clean_errors(exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )


async def json_decode_exception_handler(
        _request: Request,
        _exc: json.JSONDecodeError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid JSON format"},
    )


async def general_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
