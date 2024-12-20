from sqlalchemy.orm import Session
from domain.word.entities import Dictionary
from domain.word.entities import UserDictionary


class WordRepository:
    def __init__(self, db: Session):
        self.db = db

    async def find_my_word(self, dictionary_id: int, user_id: int):
        return (
            self.db.query(UserDictionary)
            .filter(
                UserDictionary.dictionary_id == dictionary_id,
                UserDictionary.user_id == user_id,
            )
            .first()
        )

    async def update_frequency(self, dictionary_id: int, user_id: int):
        saved_word = (
            self.db.query(UserDictionary)
            .filter(
                UserDictionary.dictionary_id == dictionary_id,
                UserDictionary.user_id == user_id,
            )
            .first()
        )
        saved_word.frequency += 1
        self.db.commit()
        self.db.refresh(saved_word)
        return saved_word

    async def save_word(self, word: str, user_id: int, dictionary_id: int):
        user_dictionary = UserDictionary(
            user_id=user_id,
            dictionary_id=dictionary_id,
        )
        self.db.add(user_dictionary)
        self.db.commit()
        self.db.refresh(user_dictionary)
        return user_dictionary

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
