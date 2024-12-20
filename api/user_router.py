from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from domain.user.response import CreateUserResponse, GetProfileResponse
from domain.user.service import UserService
from domain.user.request import CreateUserRequest, LoginUserRequest
from domain.auth.service import AuthService
from typing import Annotated
from domain.user.entities import User

router = APIRouter()

user_dependency = Annotated[User, Depends(AuthService.get_current_user)]


@router.post("/signup")
async def create_user(
    create_user_request: CreateUserRequest, db: Session = Depends(get_db)
):
    user_service = UserService(db)
    created_user = await user_service.create_user(create_user_request)

    return CreateUserResponse(
        id=created_user.user_id,
        username=created_user.username,
        email=created_user.email,
    )


@router.post("/signin")
async def login_user(
    login_user_request: LoginUserRequest, db: Session = Depends(get_db)
):
    user_service = UserService(db)
    access_token = await user_service.login_user(login_user_request)
    return access_token


@router.post("/guest")
async def login_guest(db: Session = Depends(get_db)):
    user_service = UserService(db)
    login_user_request = LoginUserRequest(username="guest", password="guest1234")
    access_token = await user_service.login_user(login_user_request)
    return access_token


@router.get("/profile")
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.get_profile(user_id)
    return GetProfileResponse(id=user.user_id, username=user.username, email=user.email)
