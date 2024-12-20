from fastapi import APIRouter, Depends
from domain.word.service import WordService
from domain.word.request import SaveWordRequest
from sqlalchemy.orm import Session
from db.database import get_db
from typing import Annotated
from domain.user.entities import User
from domain.auth.service import AuthService
from domain.word.request import TextRequest


router = APIRouter()

user_dependency = Annotated[User, Depends(AuthService.get_current_user)]


# 텍스트 분석
@router.post("/analyze")
async def analyze_text(text_request: TextRequest, db: Session = Depends(get_db)):
    word_service = WordService(db=db)
    result = await word_service.get_most_used_words(text_request.text)
    return result


@router.post("/save")
async def save_word(
    word_request: SaveWordRequest, user: user_dependency, db: Session = Depends(get_db)
):
    word_service = WordService(db=db)
    result = await word_service.save_word(word_request, user.id)
    return result


@router.get("/list")
async def get_word_list(user: user_dependency, db: Session = Depends(get_db)):
    word_service = WordService(db=db)
    result = await word_service.get_word_list(user.id)
    return result


@router.get("/search")
async def search_word_meaning(word: str, db: Session = Depends(get_db)):
    word_service = WordService(db)
    result = await word_service.search_word_meaning(word)
    return result
