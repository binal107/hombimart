from pydantic import BaseModel, EmailStr

class SignUpData(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginData(BaseModel):
    email: EmailStr
    password: str
