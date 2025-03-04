from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from domain.user.repositories import UserRepository
from sqlalchemy.orm import Session
from domain.user.entities import User

SECRET_KEY = "your-256-bit-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create_access_token(self, email: str, user_id: int, expires_min: int):
        encode = {"sub": email, "user_id": user_id}
        expires_delta = timedelta(minutes=expires_min)
        expire = datetime.now(timezone.utc) + expires_delta
        encode.update({"exp": expire})
        encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def verify_access_token(token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            if email is None or user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                )
            return {"email": email, "id": user_id}
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def authenticate_user(self, username: str, password: str):
        user = await self.repository.authenticate_user(username, password)
        if not user:
            return False
        return user

    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            if email is None or user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                )
            return User(
                user_id=payload.get("user_id"),
                email=payload.get("sub"),
                # 기타 필요한 필드들...
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    # ✅ 비밀번호 해싱 함수
    def hash_password(password: str) -> str:
        return bcrypt_context.hash(password)

    # ✅ 비밀번호 검증 함수
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt_context.verify(plain_password, hashed_password)
