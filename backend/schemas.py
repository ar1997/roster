# backend/schemas.py
from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from models import UserRole

class ShiftCreate(BaseModel):
    employee_name: str
    date: date
    start_time: time
    end_time: time

class ShiftOut(ShiftCreate):
    id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[UserRole] = UserRole.user

class UserOut(BaseModel):
    id: int
    username: str
    role: UserRole

    class Config:
        orm_mode = True
