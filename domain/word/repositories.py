from sqlalchemy.orm import Session
from domain.word.entities import Dictionary
from domain.word.request import SaveWordRequest


class WordRepository:
    def __init__(self, db: Session):
        self.db = db

    async def save_word(self, request: SaveWordRequest, user_id: int):
        dictionary = Dictionary(
            user_id=user_id,
            word=request.word,
            frequency=request.frequency,
        )
        self.db.add(dictionary)
        self.db.commit()
        self.db.refresh(dictionary)
        return dictionary

    async def get_word_list(self, user_id: int):
        words = self.db.query(Dictionary).filter(Dictionary.user_id == user_id).all()
        return words

    async def search_word(self, word: str):
        word = self.db.query(Dictionary).filter(Dictionary.word == word).first()
        return word

    async def save_dictionary(self, dictionary: Dictionary):
        print(" >>> dictionary: ", dictionary)
        self.db.add(dictionary)
        self.db.commit()
        self.db.refresh(dictionary)
        return dictionary
