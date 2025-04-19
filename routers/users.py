from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional
from models.models import User
from database.database import get_async_session
from dependencies.auth import get_current_user
from routers.auth import create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

# ===== Schemas =====
class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    cariere: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    fullname: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    cariere: Optional[str]

    class Config:
        orm_mode = True

# ===== Routes =====
@router.get("/refresh")
async def get_me(current_user: User = Depends(get_current_user)):
    access_token = create_access_token(data={"user_id": current_user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
        }
    }

@router.get("/", response_model=UserResponse)
async def get_user(
        session: AsyncSession = Depends(get_async_session),
        current_user=Depends(get_current_user)):
    return current_user


@router.put("/", response_model=UserResponse)
async def update_user(
        data: UserUpdate,
        session: AsyncSession = Depends(get_async_session),
        current_user=Depends(get_current_user)):

    for key, value in data.dict(exclude_unset=True).items():
        setattr(current_user, key, value)

    await session.commit()
    await session.refresh(current_user)
    return current_user


@router.post("/upload-image")
async def upload_profile_image(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_async_session),
        current_user=Depends(get_current_user)):
    contents = await file.read()
    current_user.profile_image = contents
    await session.commit()
    return {"message": "Profile image uploaded successfully"}

