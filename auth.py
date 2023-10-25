from fastapi import APIRouter, Depends, FastAPI, HTTPException, UploadFile, File, status, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sql_app.models import User
from datetime import datetime, timedelta
from .database import SessionLocal
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated
from sql_app import models
from sql_app.config import get_settings

# settings = get_settings()

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    responses={404: {"description": "Not found"}},
)

SECRET_KEY = "709d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    username: str
    password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

# db_dependency = Annotated[Session, Depends(get_db)]
# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def create_user(db: db_dependency,
#                       create_user_request: CreateUserRequest):
#     create_user_model = User(
#         username=create_user_request.username,
#         hashed_password=bcrypt_context.hash(create_user_request.password)
#     )

#     db.add(create_user_model)
#     db.commit()

async def get_token(data, db):
    user = db.query(User).filter(User.email == data.username).first()
    # _verify_user_access(user=user)
    return await _get_user_token(user=user)

async def create_access_token(data,  expiry: timedelta):
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload,SECRET_KEY, algorithm=ALGORITHM)

async def create_refresh_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def _get_user_token(user: User, refresh_token = None):
    payload = {"id": user.id}
    
    access_token_expiry = timedelta(minutes=30)
    
    access_token = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds  # in seconds
    )

def get_token_payload(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        return None
    return payload

async def get_refresh_token(token, db):   
    payload =  get_token_payload(token=token)
    user_id = payload.get('id', None)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await _get_user_token(user=user, refresh_token=token)

@router.post("/token", status_code=status.HTTP_200_OK)
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await get_token(data=data, db=db)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    return await get_refresh_token(token=refresh_token, db=db)

