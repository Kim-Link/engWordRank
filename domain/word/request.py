from pydantic import BaseModel, Field


class SaveWordRequest(BaseModel):
    word: str = Field(..., description="Word")
    frequency: int = Field(..., description="Frequency")
