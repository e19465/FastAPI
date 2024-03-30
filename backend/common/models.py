from database import Base
import uuid
from sqlalchemy import Column,String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

#########################################################################################
class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#########################################################################################

# if you don't have this table in database, just in http://localhost:8000/user/likes/create_table
class Likes(Base):
    __tablename__ = "likes"

    post_id = Column(UUID(as_uuid=True),ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete='CASCADE'), primary_key=True, nullable=False)