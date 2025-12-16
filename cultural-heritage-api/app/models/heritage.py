from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class HeritageEntry(Base):
   
    __tablename__ = "heritage_entries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships for easier querying
    category = relationship("Category")
    creator = relationship("User")

    def __repr__(self):
        return f"<HeritageEntry(id={self.id}, title='{self.title}', category_id={self.category_id})>"
