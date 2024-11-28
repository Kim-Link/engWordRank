from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginUserRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
