from typing import Counter, List, Dict
import spacy
from sqlalchemy.orm import Session
from domain.word.request import SaveWordRequest
from domain.word.repositories import WordRepository
from domain.openai.service import OpenAiService
import requests
import aiohttp
from bs4 import BeautifulSoup

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

    # 단어 저장
    async def save_word(self, request: SaveWordRequest, user_id: int):
        if not self.db:
            raise ValueError("Database connection is required for this operation")
        return await self.repository.save_word(request, user_id)

    # 단어 목록 조회
    async def get_word_list(self, user_id: int):
        return await self.repository.get_word_list(user_id)

    # 단어 뜻 검색
    async def search_word_meaning(self, word: str):
        result = await self.openai_service.get_completion(word)
        print("result >> ", result)
        return result

    # 단어 뜻을 네이버 사전에서 검색
    async def search_word_meaning_naver(self, word: str):
        result = await self.naver_search(word)
        print("result >> ", result)
        return result

    async def naver_search(self, word: str):
        try:
            url = "https://en.dict.naver.com/#/search"
            params = {
                "query": word,
                "range": "all",
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    html_content = await response.text()

                    # BeautifulSoup로 HTML 파싱
                    soup = BeautifulSoup(html_content, "html.parser")

                    # 특정 div 클래스 필터링
                    filtered_divs = soup.find_all("div", class_="row ")
                    print("filtered_divs >> ", filtered_divs)

                    # 필터링된 결과를 리스트로 반환
                    return [str(div) for div in filtered_divs]
        except Exception as e:
            print("error >> ", e)
            return None
