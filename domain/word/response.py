from pydantic import BaseModel


class SearchWordMeaningResponse(BaseModel):
    word: str
    word_class: str
    kr_meaning: str
    en_meaning: str
    example: str
