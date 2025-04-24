from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel
from typing import Optional
from models.models import User, Project, Skill, Connection, ProblemAndAnswer
from database.database import get_async_session
from dependencies.auth import get_current_user
from routers.auth import create_access_token
# Datetime
from datetime import datetime
router = APIRouter(prefix="/users", tags=["Users"])

# ===== Schemas =====
class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    cariere: Optional[str] = None
    startuplar: Optional[list] = None
    loyihalar: Optional[list] = None
    solve_to_problems: Optional[list] = None
    skills: Optional[list] = None
    asosiy_loyiha: Optional[str] = None
    position: Optional[int] = None
    profession: Optional[int] = None
    connections_list: Optional[list] = None
    birth_day: Optional[datetime] = None
    hozirgi_faoliyat: Optional[str] = None



class UserResponse(BaseModel):
    id: int
    username: str
    fullname: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    cariere: Optional[str]
    birth_day: Optional[datetime]
    startuplar: Optional[list]
    loyihalar: Optional[list]
    solve_to_problems: Optional[list]
    skills: Optional[list]
    asosiy_loyiha: Optional[str]
    position: Optional[int]
    profession: Optional[int]
    connections_list: Optional[list]
    birth_day: Optional[datetime]
    hozirgi_faoliyat: Optional[str]


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
    if data.startuplar is not None:
        # Startuplar listni Tozalash
        startuplar = []
        for id in data.startuplar:
            if id in current_user.startuplar:
                startuplar.append(id)
        # Startuplar database dan tozalash
        for id in current_user.startuplar:
            if id not in startuplar:
                await session.execute(delete(Project).where(Project.id == id))
        data.startuplar = startuplar
    if data.loyihalar is not None:
        # Loyihalar listni Tozalash
        loyihalar = []
        for id in data.loyihalar:
            if id in current_user.loyihalar:
                loyihalar.append(id)
        # Loyihalar database dan tozalash
        for id in current_user.loyihalar:
            if id not in loyihalar:
                await session.execute(delete(Project).where(Project.id == id))
        data.loyihalar = loyihalar
    if data.skills is not None:
        # Skillarni listini Tozalash
        skills = []
        for id in data.skills:
            if id in current_user.skills:
                skills.append(id)
        # Skills database dan tozalash
        for id in current_user.skills:
            if id not in skills:
                await session.execute(delete(Skill).where(Skill.id == id))
        data.skills = skills
    if data.solve_to_problems is not None:
        # Solve_to_problems listini Tozalash
        solve_to_problems = []
        for id in data.solve_to_problems:
            if id in current_user.solve_to_problems:
                solve_to_problems.append(id)
        # Solve_to_problems database dan tozalash
        for id in current_user.solve_to_problems:
            if id not in solve_to_problems:
                await session.execute(delete(ProblemAndAnswer).where(ProblemAndAnswer.id == id))
        data.solve_to_problems = solve_to_problems

    if data.connections_list is not None:
        # Connections listini Tozalash
        connections_list = []
        for id in data.connections_list:
            if id in current_user.connections_list:
                connections_list.append(id)
        # Connections database dan tozalash
        for id in current_user.connections_list:
            if id not in connections_list:
                await session.execute(delete(Connection).where(Connection.id == id))
        data.connections_list = connections_list

    try:
        if data.birth_day.tzinfo is not None:
            data.birth_day = data.birth_day.replace(tzinfo=None)
    except:
        pass

    for key, value in data.dict(exclude_unset=True).items():
        if value is not None:
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

