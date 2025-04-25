from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional, List
from models.models import Skill, SkillType, Language, Profession
from database.database import get_async_session
from dependencies.auth import get_current_user

router = APIRouter(prefix="/skills", tags=["Skills"])
# Scill create
class SkillCreate(BaseModel):
    type: Optional[int] = None
    grade: Optional[int] = None
    bio: Optional[str] = None

class SkillOut(SkillCreate):
    id: int
    class Config:
        orm_mode = True


@router.post("/", response_model=SkillOut)
async def create_skill(
    skill: SkillCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user)
):
    new_skill = Skill(**skill.dict(), user_id=current_user.id)
    session.add(new_skill)
    if current_user.skills is None:
        current_user.skills = []
    current_user.skills.append(new_skill.id)
    await session.commit()
    await session.refresh(new_skill)
    return new_skill




# Scill type create
class SkillTypeCreate(BaseModel):
    id: int
    name: str
    be_grade: bool

class SkillTypeOut(SkillTypeCreate):
    id: int
    class Config:
        orm_mode = True

# Get skill types

@router.get("/types", response_model=List[SkillTypeOut])
async def get_all_skill_types(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(SkillType))
    return result.scalars().all()






# Scill type create
class LanguageCreate(BaseModel):
    id: int
    name: str
    view_key: str

class LanguageOut(LanguageCreate):
    id: int
    class Config:
        orm_mode = True

# Get skill types

@router.get("/AllProgrammingLanguages", response_model=List[LanguageOut])
async def get_all_languages(
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(Language))
    return result.scalars().all()

# Get all professions

@router.get("/AllProfessions", response_model=List[Profession])
async def get_all_professions(
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(Profession))
    return result.scalars().all()
