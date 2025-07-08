from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from models.models import User
from database.database import get_async_session
from pydantic import BaseModel, Field

# ==== ROUTER ====
router = APIRouter(prefix="/auth", tags=["Auth"])

# ==== JWT SETTINGS ====
from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# ==== PAROL HASHING ====
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ==== JWT TOKEN YARATISH ====
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ==== SCHEMAS ====
class UserCreate(BaseModel):
    username: str
    password: str
    fullname: str
    email: str
    phone_number: str
    joylashuv: int
    kasb: int
    birth_day: datetime = Field(..., example="YYYY-MM-DD")
    hozirgi_faoliyat: str
    cariere: str


class UserResponse(BaseModel):
    id: int
    username: str
    fullname: str
    email: str
    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ==== ROUTES ====

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    user_exists = await session.execute(select(User).where(User.username == user.username))
    if user_exists.scalars().first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    email_exists = await session.execute(select(User).where(User.email == user.email))
    if email_exists.scalars().first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        fullname=user.fullname,
        email=user.email,
        phone_number=user.phone_number,
        position=user.joylashuv,
        profession=user.kasb,
        birth_day=user.birth_day,
        hozirgi_faoliyat=user.hozirgi_faoliyat,
        cariere=user.cariere
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    query = await session.execute(select(User).where(User.username == form_data.username))
    db_user = query.scalars().first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token}
