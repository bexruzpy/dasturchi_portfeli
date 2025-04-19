from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import User, Project
from database.database import get_async_session
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(tags=["Public Profile"])

class PublicProject(BaseModel):
    id: int
    name: str
    about_html: str
    class Config:
        orm_mode = True

class PublicUserProfile(BaseModel):
    id: int
    username: str
    fullname: str
    cariere: Optional[str]
    email: Optional[str]
    projects: List[PublicProject]

    class Config:
        orm_mode = True

@router.get("/@{username}", response_model=PublicUserProfile)
async def view_public_profile(username: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # loyihalar idlari asosida olish
    projects = []
    if user.loyihalar:
        result = await session.execute(select(Project).where(Project.id.in_(user.loyihalar)))
        projects = result.scalars().all()

    return {
        "id": user.id,
        "username": user.username,
        "fullname": user.fullname,
        "cariere": user.cariere,
        "email": user.email,
        "projects": projects
    }
