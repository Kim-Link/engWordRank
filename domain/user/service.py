from domain.user.repositories import UserRepository
from domain.user.request import CreateUserRequest, LoginUserRequest
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db

db_dependency = Annotated[Session, Depends(get_db)]


class UserService:

    # 회원가입
    def create_user(db: db_dependency, create_user_request: CreateUserRequest):
        created_user = UserRepository.create_user(db, create_user_request)
        return created_user

    # 로그인
    def login(db: db_dependency, login_user_request: LoginUserRequest):
        return login_user_request

    # 로그아웃
    def logout():
        return {}

    # 프로필 조회
    def get_profile():
        return {}

    # 회원탈퇴
    def delete_user():
        return {}
