import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from app.core import settings
from typing import Dict, Optional
from app.schemas.response import ApiResponse

router = APIRouter()

class LoginRequest(BaseModel):
    password: str


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=settings.admin.token_expire_hours)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.admin.secret_key, algorithm="HS256")
    return encoded_jwt

@router.post("/login", response_model=ApiResponse[Dict[str, str]])
async def login(request: LoginRequest):
    if request.password != settings.admin.admin_password:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token = create_access_token({"sub": "admin"})
    return ApiResponse(data={"token": token})

@router.get("/verify")
async def verify_token():
    # 如果能走到这里，说明中间件已经校验通过了
    return {"status": "success", "message": "Token is valid"}
