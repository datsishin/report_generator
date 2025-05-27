from fastapi import APIRouter

from app.schemas.input import TestInput

router = APIRouter(
    tags=["Report generator service"],
)


@router.post("/create_report")
def create_report(user_data: TestInput) -> dict[str, str]:
    return {"message": "Report created", "user_data": user_data.dict()}
