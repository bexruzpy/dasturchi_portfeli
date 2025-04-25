from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Dict, Optional, Any
from models.models import Project
from database.database import get_async_session
from dependencies.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

class ProjectCreate(BaseModel):
    name: str
    about_text: str
    about_html: str
    files: Optional[Dict[str, Dict[str, bytes]]] = None  # folder[file_name]: {"content": bytes}
    result: Optional[bytes] = None

class ProjectOut(ProjectCreate):
    id: int
    class Config:
        orm_mode = True

@router.post("/startup", response_model=ProjectOut)
async def create_project(project: ProjectCreate, session: AsyncSession = Depends(get_async_session),
        current_user=Depends(get_current_user)):
    new_project = Project(**project.dict(), user_id=current_user.id)
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    if current_user.startuplar is None:
        current_user.startuplar = []
    current_user.startuplar.append(new_project.id)
    setattr(current_user, "startuplar", current_user.startuplar+[new_project.id])
    await session.commit()
    return new_project
@router.post("/loyiha", response_model=ProjectOut)
async def create_project(project: ProjectCreate, session: AsyncSession = Depends(get_async_session),
        current_user=Depends(get_current_user)):
    new_project = Project(**project.dict(), user_id=current_user.id)
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)
    if current_user.loyihalar is None:
        current_user.loyihalar = []
    setattr(current_user, "loyihalar", current_user.loyihalar+[new_project.id])
    await session.commit()
    return new_project

@router.get("/{id}", response_model=ProjectOut)
async def get_project(
        id: int,
        session: AsyncSession = Depends(get_async_session),
        current_user=Depends(get_current_user)):
    result = await session.execute(select(Project).where(Project.id == id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/", response_model=list[ProjectOut])
async def list_projects(session: AsyncSession = Depends(get_async_session),
        current_user=Depends(get_current_user)):
    return (current_user.loyihalar or []) + (current_user.startuplar or [])
