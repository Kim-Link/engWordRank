from domain.user.repositories import UserRepository
from domain.user.request import CreateUserRequest, LoginUserRequest
from sqlalchemy.orm import Session
from domain.auth.service import AuthService
from fastapi import HTTPException
import httpx
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import json

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    # 회원가입
    async def create_user(self, create_user_request: CreateUserRequest):
        return await self.repository.create_user(create_user_request)

    # 로그인
    async def login_user(self, login_user_request: LoginUserRequest):
        username = login_user_request.username
        password = login_user_request.password
        user = await self.repository.authenticate_user(username, password)
        if not user:
            return None

        print(user.email, user.user_id)
        get_access_token = AuthService.create_access_token(
            self, email=user.email, user_id=user.user_id, expires_min=30
        )

        return get_access_token

    # 프로필 조회
    async def get_profile(self, user_id: int):
        return await self.repository.get_user_by_id(user_id)

    # 회원탈퇴
    async def delete_user():
        return {}


class UserServiceBySupabase:

    # 유저 생성(CREATE)
    @staticmethod
    async def create_user(username: str, email: str, password: str):
        password_hash = AuthService.hash_password(password)
        data = {"username": username, "email": email, "password": password_hash}
        print(SUPABASE_URL)

        async with httpx.AsyncClient(
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
        ) as client:
            response = await client.post(f"{SUPABASE_URL}/rest/v1/user", json=data)

        print(f"🔹 Supabase API 요청: {SUPABASE_URL}/rest/v1/users")
        print(f"🔹 요청 데이터: {data}")
        print(f"🔹 응답 코드: {response.status_code}")
        print(f"🔹 응답 내용: {response.text}")

        if response.status_code != 201:
            raise HTTPException(
                status_code=response.status_code, detail=str(response.text)
            )

        created_user = response.json()[0]
        user_id = created_user["id"]  # user_id 추출

        return {"message": "User created successfully", "user_id": user_id}
