from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from domain.auth.service import AuthService
from domain.user.service import UserService
from sqlalchemy.orm import Session
from db.database import get_db
from fastapi import HTTPException
from datetime import timedelta

router = APIRouter()


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    try:
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(form_data.username, form_data.password)

        if not user:
            raise HTTPException(
                status_code=401, detail="이메일 주소나 비밀번호가 올바르지 않습니다"
            )

        expires_delta = timedelta(minutes=30)
        token = auth_service.create_access_token(
            user.email, user.id, expires_delta=expires_delta
        )
        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        print(f"로그인 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="인증 처리 중 오류가 발생했습니다")
