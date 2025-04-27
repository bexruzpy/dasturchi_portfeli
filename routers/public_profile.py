from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import (
    User,
    Project,
    Connection,
    ConnectionType,
    Skill,
    ProblemAndAnswer,
    Joylashuv
)
from database.database import get_async_session
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import selectinload
from datetime import datetime
# Import for file responce
from fastapi import Response
import io


router = APIRouter(tags=["Public Profile"])

class PublicUserProfile(BaseModel):
    id: int
    username: str
    fullname: str
    hozirgi_faoliyat: str
    age: int
    email: Optional[str]
    loyihalar: List[dict]
    problems: List[dict]
    joylashuv: str
    kasb: str
    connections: List[dict]
    skills: List[dict]
    skills_list_by_id: List[int]
    asosiy_loyiha: str
    experience: str
    class Config:
        orm_mode = True

@router.get("/@{username}", response_model=PublicUserProfile)
async def view_public_profile(username: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(User)
        .options(selectinload(User.joylashuv))
        .options(selectinload(User.kasb))
        .where(User.username == username)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # connecionslarni sozlash
    all_connnections = []
    for connection_id in user.connections_list or []:
        result = await session.execute(
            select(Connection)
            .options(selectinload(Connection.connection_type))
            .where(Connection.id == connection_id)
        )
        connection = result.scalars().first()
        if connection:
            all_connnections.append(
                connection.get_public_json()
            )
    # barcha skillarni olish
    all_skills = []
    for skill_id in user.skills or []:
        result = await session.execute(
            select(Skill)
            .options(selectinload(Skill.skill_type))
            .where(Skill.id == skill_id)
        )
        skill = result.scalars().first()
        if skill:
            all_skills.append(
                skill.get_public_json()
            )
    # Barcha broject izohlarini olish 200
    all_projects = []
    for project_id in (user.startuplar or []):
        result = await session.execute(select(Project).where(Project.id == project_id))
        project = result.scalars().first()
        if project:
            all_projects.append(
                project.get_public_json(True)
            )
    for project_id in (user.loyihalar or []):
        result = await session.execute(select(Project).where(Project.id == project_id))
        project = result.scalars().first()
        if project:
            all_projects.append(
                project.get_public_json(False)
            )
    # Barcha poblema va unga yechimlarni olish
    all_problems = []
    for problem_id in user.solve_to_problems or []:
        result = await session.execute(
            select(ProblemAndAnswer)
            .where(ProblemAndAnswer.id == problem_id)
        )
        problem = result.scalars().first()
        if problem:
            all_problems.append(
                problem.get_public_json()
            )
    print((datetime.now() - user.birth_day).days // 365)
    return {
        "id": user.id,
        "username": user.username,
        "fullname": user.fullname,
        "age": (datetime.now() - user.birth_day).days // 365,
        "email": user.email,
        "joylashuv": user.joylashuv.name,
        "loyihalar": all_projects,
        "problems": all_problems,
        "kasb": user.kasb.name,
        "connections": all_connnections,
        "skills_list_by_id": user.skills or [],
        "skills": all_skills,
        "asosiy_loyiha": user.asosiy_loyiha or "",
        "hozirgi_faoliyat": user.hozirgi_faoliyat or "",
        "experience": user.experience or ""
    }
# Profile image get api
@router.get("/@{username}/avatar")
async def get_profile_image(username: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # user.profile_image : bytes
    return Response(content=user.profile_image, media_type="image/png")
# Profile cariere html
@router.get("/{username}/cariere")
async def get_project_about(username: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(content=user.cariere, media_type="text/html")



# Connection types icons
@router.get("/connection_types/{type_id}")
async def get_connection_types(type_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ConnectionType).where(ConnectionType.id == type_id))
    return Response(content=result.scalars().first().icon, media_type="image/png")


@router.get("/project/{project_id}/about")
async def get_project_about(project_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Project).where(Project.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return Response(content=project.about_html, media_type="text/html")

@router.get("/problem/{project_id}/about")
async def get_project_about(project_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ProblemAndAnswer).where(ProblemAndAnswer.id == project_id))
    problem = result.scalars().first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return Response(content=problem.problem, media_type="text/html")

@router.get("/problem/{project_id}/code")
async def get_project_about(project_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(ProblemAndAnswer)
        .options(selectinload(ProblemAndAnswer.language_ref))
        .where(ProblemAndAnswer.id == project_id))
    problem = result.scalars().first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem.get_code_json()



# Joylashuvlar type create
class JoylashuvCreate(BaseModel):
    id: int
    name: str

class JoylashuvOut(JoylashuvCreate):
    id: int
    class Config:
        orm_mode = True
# Get all Joylashuvlar
@router.get("/AllJoylashuvlar", response_model=List[JoylashuvOut])
async def get_all_professions(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Joylashuv))
    return result.scalars().all()
