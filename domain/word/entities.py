from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, ARRAY
from db.database import Base


class Dictionary(Base):
    __tablename__ = "dictionary"

    dictionary_id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), nullable=False)
    word_class = Column(String(10), nullable=False)
    kr_meaning = Column(String(500), nullable=False)
    en_meaning = Column(String(500), nullable=False)
    example = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


class UserDictionary(Base):
    __tablename__ = "user_dictionary"

    user_dictionary_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    dictionary_id = Column(Integer, ForeignKey("dictionary.dictionary_id"))
    frequency = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
