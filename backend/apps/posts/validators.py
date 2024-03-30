from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from datetime import datetime


class PostBaseValidator(BaseModel):
    title: str
    content: str
    published: bool = True

#############################! Request validation ############################

# validate requst body when creting post, check are there all field we need
class CreatePostValidator(PostBaseValidator):
    pass

# validate request body for patch request, what are the fields we need
class UpdatePostValidator(PostBaseValidator):
    pass




#############################! Response validation ############################

# Response validation for after creating (we can add or remove any field as we wish)
class CreatePostResponseValidator(PostBaseValidator):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)

    # Enable ORM
    class Config:
        from_attributes = True

# Response validation for GET requests (GET all or GET one)
class GetPostResponseValidator(CreatePostResponseValidator):
    pass


# Response validation after updating value
class UpdateResponseValidator(CreatePostResponseValidator):
    pass

