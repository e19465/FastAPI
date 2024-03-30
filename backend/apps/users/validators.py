from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from uuid import UUID, uuid4



class UserRegisterValidator(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone_number: str

    @validator('password')
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserLoginValidator(BaseModel):
    username: str
    password: str


class UserAccountUpdateValidator(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @validator('password')
    def password_length(cls, v):
        if v is not None and len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
    
class UpdateddUserValidator(BaseModel):
    username: str
    email: EmailStr
    phone_number: str

class UserOwnerPostResponse(UpdateddUserValidator):
    id: UUID = Field(default_factory=uuid4)