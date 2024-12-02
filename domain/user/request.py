from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")


class LoginUserRequest(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Access token")
