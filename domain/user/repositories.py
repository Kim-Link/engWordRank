from sqlalchemy.orm import Session
from domain.user.entities import User
from domain.user.request import CreateUserRequest
from typing import List


class UserRepository:
    def create_user(self, db: Session, user: CreateUserRequest) -> User:
        db_user = User(
            username=user.username, email=user.email, password_hash=user.password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def delete_user(self, user_id: int):
        self.db.query(User).filter(User.id == user_id).delete()
        self.db.commit()

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()
