from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from db.database import Base


class TextAnalysisResult(Base):
    id: int
    user_id: int
    word: str
    frequency: int
    phrase: str
