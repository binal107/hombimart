from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from app.schemas.user import SignUpData, LoginData
from app.services.auth_service import signup_user, login_user, get_user_profile

router = APIRouter()

@router.post("/signup")
async def signup(user: SignUpData):
    return await signup_user(user)

@router.post("/login")
async def login(user: LoginData):
    return await login_user(user)

@router.get("/profile")
async def profile(Authorization: Optional[str] = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    return await get_user_profile(Authorization)
