from fastapi import FastAPI
from api.text_router import router as text_router
from api.pdf_router import router as pdf_router
from api.user_router import router as user_router
from db.database import engine
from domain.user.entities import Base as UserBase
from domain.text.entities import Base as TextBase
from domain.pdf.entities import Base as PDFBase

app = FastAPI()

# 라우터 연결
app.include_router(text_router, prefix="/text", tags=["text"])
app.include_router(pdf_router, prefix="/pdf", tags=["pdf"])
app.include_router(user_router, prefix="/user", tags=["user"])

# 데이터베이스 테이블 생성
UserBase.metadata.create_all(bind=engine)
TextBase.metadata.create_all(bind=engine)
PDFBase.metadata.create_all(bind=engine)

@app.get("/health")
async def health():
    return {"status": "ok"}

