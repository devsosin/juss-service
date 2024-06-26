# https://github.com/YeoouByeol/CommerceWeb-Back

from typing import Optional

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from database import models
from database.conn import engine

# ---------------------------------------------------------------------------------------------
# Before Server ON

try:
    import asyncio
    from sqlalchemy.sql import text
    async def test_database_connection():
        # 비동기 세션 생성
        async with engine.begin() as conn:
            # 간단한 쿼리 실행
            result = await conn.execute(text("SELECT 1"))
            # 결과 출력
            print(result.scalar())

    # 이벤트 루프를 사용하여 비동기 함수 실행
    asyncio.run(test_database_connection())
    
    # session
    print('DB Connected')
except Exception as e:
    print('DB Connection Error')
    print(e)

# ---------------------------------------------------------------------------------------------
# Server Setting

app = FastAPI()

# 데이터베이스 초기화
@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

# 테이블 TRUNCATE
# SET FOREIGN_KEY_CHECKS = 0;
# TRUNCATE tb_user;

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------------------------
# Router Setting

test_router = APIRouter()
@test_router.get('')
async def root(request: Request):
    return {'msg': 'Hello World'}

from routes import users, datas, accounts, transactions, transfer, cards

app.include_router(test_router, prefix='/api/v1')
app.include_router(users.router, prefix='/api/v1')
app.include_router(datas.router, prefix='/api/v1')
app.include_router(accounts.router, prefix='/api/v1')
app.include_router(transactions.router, prefix='/api/v1')
app.include_router(transfer.router, prefix='/api/v1')
app.include_router(cards.router, prefix='/api/v1')

# ---------------------------------------------------------------------------------------------
# Memos

# bigger application (한번 쯤 읽어보면 좋음)
# https://fastapi.tiangolo.com/tutorial/bigger-applications/

# python3 -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
