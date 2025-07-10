from fastapi import HTTPException
from app.schemas.user import SignUpData, LoginData
from app.supabase_client import get_supabase_client

client, headers, SUPABASE_URL = get_supabase_client()

async def signup_user(user: SignUpData):
    async with client:
        response = await client.post(
            f"{SUPABASE_URL}/auth/v1/signup",
            headers=headers,
            json={"email": user.email, "password": user.password}
        )
    if response.status_code in [200, 201]:
        return {"message": "Signup successful. Please check your email to confirm."}
    try:
        error_detail = response.json()
    except Exception:
        error_detail = response.text
    raise HTTPException(status_code=response.status_code, detail=error_detail)

async def login_user(user: LoginData):
    async with client:
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
    try:
        error_detail = response.json()
    except Exception:
        error_detail = response.text
    raise HTTPException(status_code=response.status_code, detail=error_detail)

async def get_user_profile(token: str):
    async with client:
        response = await client.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={
                "Authorization": token,
                "apikey": headers["apikey"]
            }
        )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail="Invalid token")
