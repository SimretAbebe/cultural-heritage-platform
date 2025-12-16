from sqlalchemy import Column, Integer, String, Text

from app.database import Base

class Category(Base):
   
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
