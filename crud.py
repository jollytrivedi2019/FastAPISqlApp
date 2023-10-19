from sqlalchemy.orm import Session

from . import models, schemas


def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.id == file_id).first()


def get_file_by_name(db: Session, filename: str):
    return db.query(models.File).filter(models.File.filename == filename).first()


def get_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.File).offset(skip).limit(limit).all()


def create_file(db: Session, file: schemas.FileCreate):
    # fake_hashed_password = file.password + "notreallyhashed"
    db_file = models.File(filename=file.filename)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file



