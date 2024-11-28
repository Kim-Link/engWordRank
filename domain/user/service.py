from domain.user.repositories import UserRepository
from domain.user.request import CreateUserRequest, LoginUserRequest
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db

db_dependency = Annotated[Session, Depends(get_db)]


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    # 회원가입
    def create_user(self, create_user_request: CreateUserRequest):
        return self.repository.create_user(create_user_request)

    # 로그인
    def login(self, login_user_request: LoginUserRequest):
        return self.repository.login(login_user_request)

    # 로그아웃
    def logout():
        return {}

    # 프로필 조회
    def get_profile():
        return {}

    # 회원탈퇴
    def delete_user():
        return {}
