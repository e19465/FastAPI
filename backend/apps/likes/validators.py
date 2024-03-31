from pydantic import BaseModel, Field
from uuid import UUID, uuid4



class CreateLikeValidator(BaseModel):
    post_id: UUID = Field(default_factory=uuid4)
    direction: bool = Field(..., description="Indicates whether the like is positive (True) or negative (False)")

