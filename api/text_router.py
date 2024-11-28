from fastapi import APIRouter

router = APIRouter(
    prefix="/text",
    tags=["text"],
)


# 텍스트 분석
@router.post("/analyze")
def analyze_text(text: str):
    return {"text": text}
