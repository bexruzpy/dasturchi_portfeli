from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from models.models import Connection
from database.database import get_async_session
from dependencies.auth import get_current_user

router = APIRouter(prefix="/connections", tags=["Connections"])

class ConnectionCreate(BaseModel):
    type: int
    name: str
    datas: Dict[str, Any]

class ConnectionOut(ConnectionCreate):
    id: int
    class Config:
        orm_mode = True

@router.post("/", response_model=ConnectionOut)
async def add_connection(
    data: ConnectionCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user)
):
    conn = Connection(**data.dict())
    session.add(conn)
    await session.commit()
    await session.refresh(conn)
    return conn

@router.get("/", response_model=List[ConnectionOut])
async def list_connections(
    session: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user)
):
    result = await session.execute(select(Connection))
    return result.scalars().all()
