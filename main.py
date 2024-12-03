from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from api.word_router import router as word_router
from api.user_router import router as user_router
from api.auth_router import router as auth_router
from db.database import engine
from domain.user.entities import Base as UserBase

app = FastAPI(debug=True)
app.add_middleware(
    DebugToolbarMiddleware,
    panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
)
# 라우터 연결
app.include_router(word_router, prefix="/word", tags=["word"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(auth_router, prefix="/token", tags=["token"])

# 데이터베이스 테이블 생성
UserBase.metadata.create_all(bind=engine)


@app.get("/health")
async def health():
    return {"status": "ok"}
