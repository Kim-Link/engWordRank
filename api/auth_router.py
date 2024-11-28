from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from domain.user.service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


# @router.post("/token")
# def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user = UserService.login(form_data)
#     return {"form_data": form_data}
