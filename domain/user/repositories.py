from sqlalchemy.orm import Session
from domain.user.entities import User
from domain.user.request import CreateUserRequest
from typing import List
from passlib.context import CryptContext
from fastapi import HTTPException

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user: CreateUserRequest) -> User:
        existing_user = await self.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        db_user = User(
            username=user.username,
            email=user.email,
            password_hash=bcrypt_context.hash(user.password),
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    async def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    async def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.user_id == user_id).first()

    async def delete_user(self, user_id: int):
        self.db.query(User).filter(User.user_id == user_id).delete()
        self.db.commit()

    async def get_all_users(self) -> List[User]:
        return self.db.query(User).all()

    async def authenticate_user(self, username: str, password: str):
        print("username!!!!!!!!!", username)
        user = await self.get_user_by_username(username)
        if not user:
            return False
        if not bcrypt_context.verify(password, user.password_hash):
            return False
        return user
