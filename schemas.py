from pydantic import BaseModel


class FileBase(BaseModel):
    filename: str


class FileCreate(FileBase):
    filedetails: str


class File(FileBase):
    id: int
   
    class Config:
        orm_mode = True
