from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from domain.user.response import CreateUserResponse, GetProfileResponse
from domain.user.service import UserService
from domain.user.request import CreateUserRequest, LoginUserRequest

router = APIRouter()


@router.post("/signup")
async def create_user(
    create_user_request: CreateUserRequest, db: Session = Depends(get_db)
):
    user_service = UserService(db)
    created_user = await user_service.create_user(create_user_request)

    return CreateUserResponse(
        id=created_user.id, username=created_user.username, email=created_user.email
    )


@router.get("/profile")
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.get_profile(user_id)
    return GetProfileResponse(id=user.id, username=user.username, email=user.email)
