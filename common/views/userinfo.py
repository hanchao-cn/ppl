# Encoding: UTF-8
from binascii import a2b_qp
from datetime import datetime
from venv import logger
from quart import current_app
from sqlalchemy import select, update
from common.db.models.user import user

class userinfo():
    def __init__(self):
        dbsession=current_app.db.get_session()
        self.newsession=dbsession()


    #判断用户是否存在
    async def isUserExist(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        result=await self.newsession.execute(select(user).filter_by(wx_openid=openid))
        await self.newsession.commit()
        if result.fetchone() is None:
            return False
        else:
            return True
    #添加用户
    async def addUser(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        try:
            if not await self.isUserExist(openid):
                newuser=user(wx_openid=openid)
                self.newsession.add(newuser)
                await self.newsession.commit()
                await self.newsession.close()
        finally:
            await self.newsession.close()      
        return True
    
    #获取user.chat_count并减1再更新user.chat_count
    async def reduc_chat_count(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")       
        result=await self.newsession.execute(select(user.chat_count).filter_by(wx_openid=openid))
        count=result.scalars().first()
        await self.newsession.execute(update(user).where(user.wx_openid==openid).values(chat_count=count-1))
        await self.newsession.commit()
        await self.newsession.close()
        return count-1
    
    #获取user.img_count并减1再更新user.img_count
    async def reduc_img_count(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        result=await self.newsession.execute(select(user.img_count).filter_by(wx_openid=openid))
        count=result.scalars().first()
        await self.newsession.execute(update(user).where(user.wx_openid==openid).values(img_count=count-1))
        await self.newsession.commit()
        await self.newsession.close()
        return count-1
    #获取user.voice_count并减1再更新user.voice_count
    async def reduc_voice_count(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        result=await self.newsession.execute(select(user.Voice_count).filter_by(wx_openid=openid))
        count=result.scalars().first()
        await self.newsession.execute(update(user).where(user.wx_openid==openid).values(Voice_count=count-1))
        await self.newsession.commit()
        await self.newsession.close()
        return count-1
    
    #获取user.chat_count并加1再更新user.chat_count
    async def add_chat_count(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        result= await self.newsession.execute(select(user.chat_count).filter_by(wx_openid=openid))
        count=result.scalars().first()
        await self.newsession.execute(update(user).where(user.wx_openid==openid).values(chat_count=count+1))
        await self.newsession.commit()
        await self.newsession.close()
        return count+1
    #获取user.img_count并加1再更新user.img_count
    async def add_img_count(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        result=await self.newsession.execute(select(user.img_count).filter_by(wx_openid=openid))
        count=result.scalars().first()
        await self.newsession.execute(update(user).where(user.wx_openid==openid).values(img_count=count+1))
        await self.newsession.commit()
        await self.newsession.close()
        return count+1
    #获取user.voice_count并加1再更新user.voice_count
    async def add_voice_count(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        result=await self.newsession.execute(select(user.Voice_count).filter_by(wx_openid=openid))
        count=result.scalars().first()
        await self.newsession.execute(update(user).where(user.wx_openid==openid).values(Voice_count=count+1))
        await self.newsession.commit()
        await self.newsession.close()
        return count+1
    
    #更新user.role
    async def set_role(self,openid,role):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        await self.newsession.execute(update(user).where(user.wx_openid==openid).values(role=role))
        await self.newsession.commit()
        await self.newsession.close()
    
    #更新user.login_time
    async def update_login_time(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        await self.newsession.execute(update(user).where(user.wx_openid==openid).values(login_time=datetime.datetime.now()))
        await self.newsession.commit()
        await self.newsession.close()
    
    #获取user.role
    async def get_role(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        result=await self.newsession.execute(select(user.role).filter_by(wx_openid=openid))
        role=result.scalars().first()
        await self.newsession.commit()
        await self.newsession.close()
        return role
    #更新登陆时间
    async def update_login_time(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        await self.newsession.execute(update(user).where(user.wx_openid==openid).values(login_time=datetime.now()))
        await self.newsession.commit()
        await self.newsession.close()
    #获取剩余聊天次数
    async def get_chat_count(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        result=await self.newsession.execute(select(user.chat_count).filter_by(wx_openid=openid))
        count=result.scalars().first()
        await self.newsession.commit()
        await self.newsession.close()
        return count
    #获取剩余图片次数
    async def get_img_count(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        result=await self.newsession.execute(select(user.img_count).filter_by(wx_openid=openid))
        count=result.scalars().first()
        await self.newsession.commit()
        await self.newsession.close()
        return count
    #获取剩余语音次数
    async def get_voice_count(self,openid):
        if self.newsession is None:
            raise ValueError("newsession is not initialized")
        result=await self.newsession.execute(select(user.Voice_count).filter_by(wx_openid=openid))
        count=result.scalars().first()
        await self.newsession.commit()
        await self.newsession.close()
        return count
    
    