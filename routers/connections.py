from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from models.models import Connection, ConnectionType
from database.database import get_async_session
from dependencies.auth import get_current_user

router = APIRouter(prefix="/connections", tags=["Connections"])

class ConnectionCreate(BaseModel):
    type: int
    datas: Dict[str, str]

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
    conn = Connection(**data.dict(), user_id=current_user.id)
    session.add(conn)
    if current_user.connections_list is None:
        current_user.connections_list = []
    current_user.connections_list.append(conn.id)
    await session.commit()
    await session.refresh(conn)
    return conn

# Connection type create
class ConnectionTypeCreate(BaseModel):
    id: int
    name: str
    datas: dict

class ConnectionTypeOut(ConnectionTypeCreate):
    id: int
    class Config:
        orm_mode = True
# Connection all types

@router.get("/AllConnectionTypes", response_model=List[ConnectionTypeOut])
async def get_all_languages(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(ConnectionType))
    return result.scalars().all()

