from domain.user.repositories import UserRepository
from domain.user.request import CreateUserRequest, LoginUserRequest
from sqlalchemy.orm import Session
from domain.auth.service import AuthService


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
