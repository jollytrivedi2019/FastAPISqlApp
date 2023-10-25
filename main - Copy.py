from fastapi import APIRouter, Depends, FastAPI, HTTPException, UploadFile, File, status
from sql_app import models
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
# from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from secrets import token_hex
from . import auth


from . import crud, schemas
from .database import SessionLocal, engine



models.Base.metadata.create_all(bind=engine)



# SECRET_KEY = "openssl rand -hex 32"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str or None = None

# class User(BaseModel):
#     username: str
#     email: str or None = None
#     full_name: str or None = None
#     disabled: bool or None = None

# class UserInDB(User):
#     hashed_password: str

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()
app.include_router(auth.router)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(db, username: str):
#     if username in db:
#         user_data = db[username]
#         return UserInDB(**user_data)

# def authenticate_user(db, username:str, password: str):
#     user = get_user(db,username)
#     if not user:
#         return False
#     if not verify_password(password,user.hashed_password):
#         return False
    
# def create_access_token(data: dict, expires_delta: timedelta or None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)

# to_encode.update({"exp": expire})
# encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
# retun encoded_jwt

# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_ext = file.filename.split(".").pop()
    file_name = token_hex(10)
    file_path = f"{file_name}.{file_ext}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"content":content, "success":True, "file_path":file_path, "message":"File uploaded successfully"}

    # return {"filename": file.filename, "username": "JT"}

    # db_file = crud.get_file_by_name(db, filename=file.filename)
    # if db_file:
    #     raise HTTPException(status_code=400, detail="Filename already exists")
    # return crud.create_file(db=db, file=file)



@app.post("/files/", response_model=schemas.File)
def create_file(file: schemas.FileCreate, db: Session = Depends(get_db)):
    db_file = crud.get_file_by_name(db, filename=file.filename)
    if db_file:
        raise HTTPException(status_code=400, detail="Filename already exists")
    return crud.create_file(db=db, file=file)


@app.get("/files/", response_model=list[schemas.File])
def read_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = crud.get_files(db, skip=skip, limit=limit)
    return files


@app.get("/files/{file_id}", response_model=schemas.File)
def read_file(file_id: int, db: Session = Depends(get_db)):
    db_file = crud.get_file(db, file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

@app.get("/download/{file_id}")
async def download_file(file_id: int):
    # Implement your logic to download files here
    # return {"message": f"Downloading file {file_id}", "username": current_user["username"]}
    return {"message": f"Downloading file {file_id}" }


