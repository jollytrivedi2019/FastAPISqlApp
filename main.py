from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # return {"filename": file.filename, "username": "JT"}

    db_file = crud.get_file_by_name(db, filename=file.filename)
    if db_file:
        raise HTTPException(status_code=400, detail="Filename already exists")
    return crud.create_file(db=db, file=file)



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

# @app.get("/download/{file_id}")
# async def download_file(file_id: int):
#     # Implement your logic to download files here
#     return {"message": f"Downloading file {file_id}", "username": current_user["username"]}


