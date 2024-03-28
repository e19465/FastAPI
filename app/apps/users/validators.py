from pydantic import BaseModel, EmailStr, validator



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


