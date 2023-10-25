from pydantic import BaseModel


class FileBase(BaseModel):
    filename: str


class FileCreate(FileBase):
    filedetails: str


class File(FileBase):
    id: int
   
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    email: str
    password: str


class User(UserBase):
    email: str
    id: int
    is_active: bool
    

    class Config:
        orm_mode = True

# class UserBase(BaseModel):
#     username: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool

#     class Config:
#         orm_mode = True


    
