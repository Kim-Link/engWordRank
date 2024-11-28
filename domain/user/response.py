from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    id: int
    username: str
    email: str
