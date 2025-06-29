from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel, EmailStr
import httpx
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

class SignUpData(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginData(BaseModel):
    email: EmailStr
    password: str

@app.post("/signup")
async def signup(user: SignUpData):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/auth/v1/signup",
            headers=headers,
            json={"email": user.email, "password": user.password}
        )
    if response.status_code in [200, 201]:
        return {"message": "Signup successful. Please check your email to confirm."}
    else:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text
        raise HTTPException(status_code=response.status_code, detail=error_detail)

@app.post("/login")
async def login(user: LoginData):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/auth/v1/token",
            headers=headers,
            json={
                "email": user.email,
                "password": user.password,
                "grant_type": "password"
            }
        )
    if response.status_code == 200:
        data = response.json()
        return {
            "access_token": data["access_token"],
            "refresh_token": data["refresh_token"],
            "user": data.get("user", {})
        }
    else:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text
        raise HTTPException(status_code=response.status_code, detail=error_detail)

@app.get("/profile")
async def profile(Authorization: Optional[str] = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={
                "Authorization": Authorization,
                "apikey": SUPABASE_KEY
            }
        )

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Invalid token")