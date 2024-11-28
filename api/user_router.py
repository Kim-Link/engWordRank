from fastapi import APIRouter
from domain.user.service import UserService
from domain.user.request import CreateUserRequest, LoginUserRequest

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

user_service = UserService()


# 회원가입
@router.post("/signup")
def signup(user: CreateUserRequest):
    return user_service.create_user(user)


# 로그인
@router.post("/login")
def login(user: LoginUserRequest):
    return user_service.login(user)


# 로그아웃
@router.post("/logout")
def logout():
    return user_service.logout()


# 프로필 조회
@router.get("/profile")
def get_profile():
    return user_service.get_profile()


# 회원탈퇴
@router.delete("/delete")
def delete_user():
    return user_service.delete_user()
