# sole to problems
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import ProblemAndAnswer, User, Language
from database.database import get_async_session
from dependencies.auth import get_current_user

router = APIRouter(prefix="/solve_to_problems", tags=["Solve To Problems"])

# add solve to problem
class ProblemAndAnswerCreate(BaseModel):
    name: str
    problem: str
    answer: str
    language: int
class ProblemAndAnswerOut(ProblemAndAnswerCreate):
    id: int

    class Config:
        orm_mode = True

@router.post("/", response_model=ProblemAndAnswerOut)
async def add_solve_to_problem(
        data: ProblemAndAnswerCreate,
        session: AsyncSession = Depends(get_async_session),
        current_user=Depends(get_current_user)
    ):
    problem = ProblemAndAnswer(**data.dict(), user_id=current_user.id)
    session.add(problem)
    await session.commit()
    await session.refresh(problem)
    # user listga qo'shish
    setattr(current_user, "solve_to_problems", current_user.solve_to_problems+[problem.id])
    await session.commit()
    return problem




