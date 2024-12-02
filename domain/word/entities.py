from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from db.database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word = Column(String(50), nullable=False)
    frequency = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
