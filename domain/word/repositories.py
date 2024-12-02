from sqlalchemy.orm import Session
from domain.word.entities import Word
from domain.word.request import SaveWordRequest


class WordRepository:
    def __init__(self, db: Session):
        self.db = db

    async def save_word(self, request: SaveWordRequest, user_id: int):
        word = Word(
            user_id=user_id,
            word=request.word,
            frequency=request.frequency,
        )
        self.db.add(word)
        self.db.commit()
        self.db.refresh(word)
        return word

    async def get_word_list(self, user_id: int):
        words = self.db.query(Word).filter(Word.user_id == user_id).all()
        return words
