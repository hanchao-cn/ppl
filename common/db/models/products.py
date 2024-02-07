from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class user(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name= Column(String(20))
    price = Column(Integer)
    description = Column(String(100))
    image = Column(String(100))
    Duration = Column(Integer)
    chat_count = Column(Integer)
    img_count = Column(Integer)
    Voice_count = Column(Integer)

    def __init__(self, name, price, description, image, Duration, chat_count, img_count, Voice_count):
        self.name = name
        self.price = price
        self.description = description
        self.image = image
        self.Duration = Duration
        self.chat_count = chat_count
        self.img_count = img_count
        self.Voice_count = Voice_count
        
    def __repr__(self):
        return f"id(id={self.id!r}, name={self.name!r}, price={self.price!r}"