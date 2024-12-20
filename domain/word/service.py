from typing import Counter
import spacy
from sqlalchemy.orm import Session
from domain.word.request import SaveWordRequest
from domain.word.repositories import WordRepository
from domain.openai.service import OpenAiService
from domain.word.entities import Dictionary


nlp = spacy.load("en_core_web_sm")


class WordService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = WordRepository(db)
        self.openai_service = OpenAiService()

    # 텍스트 분석
    async def get_most_used_words(self, text: str):
        doc = nlp(text)
        result = {}
        words = [token.text for token in doc if token.is_alpha]
        word_freq = Counter(words)
        most_common_words = word_freq.most_common()
        for word, freq in most_common_words:
            result[word] = freq
        # 단어 목록 반환
        return result

    # 단어 분석(원래 형태 복원)
    async def get_original_form(self, text: str):
        doc = nlp(text)
        return doc[0].lemma_

    # 단어 저장
    async def save_word(self, request: SaveWordRequest, user_id: int):
        word = request.word.lower()

        # 사전에 저장되어 있는 단어인지 확인
        word_info = await self.search_word_meaning(word)

        # 이미 저장한 단어인지 확인
        search_history = await self.repository.find_my_word(
            word_info.dictionary_id, user_id
        )
        if search_history:
            await self.repository.update_frequency(word_info.dictionary_id, user_id)
            return

        await self.repository.save_word(
            word, user_id, dictionary_id=word_info.dictionary_id
        )
        return "단어 저장 완료"

    # 단어 목록 조회
    async def get_word_list(self, user_id: int):
        return await self.repository.get_word_list(user_id)

    # 단어 뜻 검색
    async def search_word_meaning(self, word: str):
        word = await self.get_original_form(word.lower())
        word_result = await self.repository.search_word(word)
        if not word_result:
            new_word = await self.openai_service.get_word_info(word)
            register_word = await self.repository.save_dictionary(new_word)
            return register_word

        else:
            result = Dictionary(
                dictionary_id=word_result.dictionary_id,
                word=word_result.word,
                word_class=word_result.word_class,
                kr_meaning=word_result.kr_meaning,
                en_meaning=word_result.en_meaning,
                example=word_result.example,
            )
            return result
