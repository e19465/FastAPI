from database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


#########################################################################################


# if you don't have this table in database, just in http://localhost:8000/user/likes/create_table
class Likes(Base):
    __tablename__ = "likes"
    post_id = Column(UUID(as_uuid=True),ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete='CASCADE'), primary_key=True, nullable=False)