import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from common.db import config
from common.db.models.products import Base as productsBase
from common.db.models.user import Base as userBase


# 创建一个db类，用于操作数据库。类被创建时，会自动创建一个数据库连接池，数据库销毁时，会自动销毁连接池。
class DBPool(object):
    def __init__(self,app):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+aiomysql://{}:{}@{}/chatportal'.format(config.username,config.password,
                                                                             config.db_address)
        self.async_engine = create_async_engine(app.config['SQLALCHEMY_DATABASE_URI'], 
                                                echo=False, pool_pre_ping=True, pool_recycle=3600, pool_size=5, max_overflow=10)
        
        
    def dispose(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_engine.dispose())
        
    def __del__(self):
        self.dispose()
    
    async def create_all(self):
            async with self.async_engine.begin() as conn:
                await conn.run_sync(userBase.metadata.create_all)
                await conn.run_sync(productsBase.metadata.create_all)
    def get_session(self):
        return sessionmaker(
        self.async_engine, expire_on_commit=False, class_=AsyncSession
    )

