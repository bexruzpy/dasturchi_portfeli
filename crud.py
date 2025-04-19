from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import User, Project, Skill, SkillType, Language, ConnectionType
from passlib.context import CryptContext
from database.database import async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==== USER ====

async def get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(session: AsyncSession, user_data: dict):
    user_data["password"] = pwd_context.hash(user_data["password"])
    new_user = User(**user_data)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

# ==== PROJECT ====

async def get_project_by_id(session: AsyncSession, project_id: int):
    result = await session.execute(select(Project).where(Project.id == project_id))
    return result.scalars().first()

async def create_project(session: AsyncSession, project_data: dict):
    new_project = Project(**project_data)
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)
    return new_project

async def list_projects(session: AsyncSession):
    result = await session.execute(select(Project))
    return result.scalars().all()

# ==== SKILL ====

async def add_skill(session: AsyncSession, skill_data: dict):
    new_skill = Skill(**skill_data)
    session.add(new_skill)
    await session.commit()
    await session.refresh(new_skill)
    return new_skill

async def list_skills(session: AsyncSession):
    result = await session.execute(select(Skill))
    return result.scalars().all()

async def add_skill_type(skill_name: str, be_grade: bool, session=async_session()):
    new_skill_type = SkillType(name=skill_name, be_grade=be_grade)
    session.add(new_skill_type)
    await session.commit()
    await session.refresh(new_skill_type)
    return new_skill_type

async def list_skill_types(session: AsyncSession):
    result = await session.execute(select(Skill))
    return result.scalars().all()

# ==== LANGUAGE ===

async def add_language(language_name: str, session: AsyncSession = async_session()):
    new_language = Language(name=language_name, view_key="")
    session.add(new_language)
    await session.commit()
    await session.refresh(new_language)
    return new_language

# ==== CONNECTION ===
async def add_connection_type(name: str, datas: dict = {}, icon: bytes = None):
    async with async_session() as session:
        # Oldindan borligini tekshirish
        result = await session.execute(select(ConnectionType).where(ConnectionType.name == name))
        if result.scalars().first():
            return {"detail": f"{name} allaqachon mavjud"}

        new_type = ConnectionType(name=name, datas=datas, icon=icon)
        session.add(new_type)
        await session.commit()
        await session.refresh(new_type)
        return new_type
