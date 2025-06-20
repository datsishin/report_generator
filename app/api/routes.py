import json

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError, BaseModel
import app.services.file_service
from app.schemas.input import TestInput

router = APIRouter(
    tags=["Report generator service"],
)


@router.post("/create_report", response_model=None)
async def create_report(
        user_data: str = Form(...),
        file: UploadFile = File(...)
):
    try:
        data_dict = json.loads(user_data)  # распарсили JSON строку
        test_input = TestInput(**data_dict)  # валидируем Pydantic
        file_content = app.services.file_service.FileService.parse_file(file)
        print(f'file content = {file_content}')
        return JSONResponse({
            "status": "success",
            "data": test_input.model_dump(mode="json"),
            "filename": file.filename
        })
    except json.JSONDecodeError:
        raise HTTPException(400, detail="Invalid JSON format")
    except ValidationError as e:
        raise HTTPException(422, detail=e.errors())
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# @router.post("/create_report", response_model=None)
# async def create_report(
#     user_data: str = Form(...),
#     file: UploadFile = File(...)
# ):
#     return {"message": "ok"}
