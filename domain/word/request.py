from pydantic import BaseModel, Field


class SaveWordRequest(BaseModel):
    word: str = Field(..., description="Word")


class TextRequest(BaseModel):
    text: str = Field(..., description="Text")
