import json
from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from app.schemas.input import TestInput

router = APIRouter(
    tags=["Report generator service"],
)


@router.post("/create_report", response_model=None)
async def create_report(
        user_data: Annotated[str, Form(...)],
        file: Annotated[UploadFile, File(...)],
):
    data_dict = json.loads(user_data)
    test_input = TestInput(**data_dict)

    return JSONResponse(
        {
            "status": "success",
            "data": test_input.model_dump(mode="json"),
            "filename": file.filename,
        },
    )
