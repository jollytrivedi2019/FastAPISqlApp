from sqlalchemy.orm import Session
from sql_app.models import User

from .import models, schemas

# Get Files
def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.id == file_id).first()


def get_file_by_name(db: Session, filename: str):
    return db.query(models.File).filter(models.File.filename == filename).first()


def get_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.File).offset(skip).limit(limit).all()


def create_file(db: Session, file: schemas.FileCreate):
    db_file = models.File(filename=file.filename)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     new_user = User(
#         email=user.email,
#         hashed_password=fake_hashed_password,
#         is_active=True
#          )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
    

