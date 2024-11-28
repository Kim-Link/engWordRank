from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from domain.user.response import CreateUserResponse
from domain.user.service import UserService
from domain.user.request import CreateUserRequest, LoginUserRequest

router = APIRouter()


@router.post("/signup")
def create_user(create_user_request: CreateUserRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    created_user = user_service.create_user(create_user_request)

    return CreateUserResponse(
        id=created_user.id, username=created_user.username, email=created_user.email
    )


@router.post("/login")
def login(login_request: LoginUserRequest, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.login(login_request)
