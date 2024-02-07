import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class user(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    wx_openid = Column(String(20), unique=True, nullable=False)
    username = Column(String(20),default='')
    password = Column(String(20),default='')
    chat_count = Column(Integer,default=100)
    img_count = Column(Integer,default=100)
    Voice_count = Column(Integer,default=100)
    role = Column(Integer,default=0)
    create_time = Column(DateTime)
    login_time = Column(DateTime)
    
    def __init__(self, wx_openid,username='', password='',  
                 role=0, chat_count=100,img_count=100,Voice_count=100,
                 create_time=datetime.datetime.now(), login_time=datetime.datetime.now()):
        self.wx_openid = wx_openid
        self.username = username
        self.password = password
        self.role = role
        self.chat_count = chat_count
        self.img_count = img_count
        self.Voice_count = Voice_count
        self.create_time = create_time
        self.login_time = login_time
    
    def __repr__(self):
        return f"id={self.id!r}, wx_openid={self.wx_openid!r}, nickname={self.nickname!r},role={self.role!r},username={self.username!r},login_time={self.login_time!r})"
    
