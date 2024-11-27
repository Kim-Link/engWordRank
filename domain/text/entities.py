from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from db.database import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    word = Column(Text, nullable=False)
    frequency = Column(Integer, default=1)
    is_phrase = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

class TextInput(Base):
    __tablename__ = "text_inputs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    analyzed_at = Column(DateTime, default=func.now())

class GlobalWordRanking(Base):
    __tablename__ = "global_word_rankings"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(Text, nullable=False)
    frequency = Column(Integer, default=0)
    is_phrase = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=func.now())
