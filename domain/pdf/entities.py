from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from db.database import Base

class PDF(Base):
    __tablename__ = "pdfs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    filename = Column(String(255), nullable=False)
    s3_url = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    analyzed_at = Column(DateTime, nullable=True)
