from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker

from sosin.utils.secret import read_config

env = read_config('.env')
user = env['DB_USERNAME']

DATABASE_URL = 'mysql+aiomysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
    env['DB_USERNAME'], env['DB_PASSWORD'], env['DB_HOST'], env['DB_PORT'], env['DB_NAME']
)

engine = create_async_engine(
    DATABASE_URL,
    future=True, # echo=True,
)

from asyncio import current_task

async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
session = async_scoped_session(async_session, scopefunc=current_task)