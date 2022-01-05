from enum import Enum
from typing import Optional
from pydantic import Field, validator, BaseModel
from datetime import datetime
from uuid import UUID


def enum_to_string(cls) -> str:
    return ', '.join([f'{e.name}' for e in cls])


class Gender(Enum):
    male = 'male'
    female = 'female'


class NewStudents(BaseModel):
    name: str = Field(example='name')
    department: str = Field(example='major')
    gender: str = Field(example='gender')
    birth_date: datetime
    created_at: datetime
    updated_at: datetime


class NewStudents_Patch(BaseModel):
    name: Optional[str] = Field(example='Name')
    major: Optional[str] = Field(example='major')
    gender: Optional[str] = Field(example='gender')

    @validator('gender')
    def validate_gender(cls, value: str):
        try:
            value = Gender(value)
        except ValueError:
            ValueError('This gender is not available')
        return value


class TestDB(BaseModel):
    id: int = Field(example=1234)
    name: str
    gender: str
    department: str
    birth_date: datetime
    created_at: datetime
    updated_at: datetime
