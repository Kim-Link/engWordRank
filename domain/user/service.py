from domain.user.repositories import UserRepository
from domain.user.request import CreateUserRequest, LoginUserRequest
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    # 회원가입
    async def create_user(self, create_user_request: CreateUserRequest):
        return await self.repository.create_user(create_user_request)

    # 로그아웃
    def logout():
        return {}

    # 프로필 조회
    async def get_profile(self, user_id: int):
        return await self.repository.get_user_by_id(user_id)

    # 회원탈퇴
    async def delete_user():
        return {}
