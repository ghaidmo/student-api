from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class StudentsPost(BaseModel):
    name: str = Field(example='name', max_length=50)
    department: str = Field(example='major')
    gender: str = Field(example='gender')
    state: str = Field(example='state')
    birth_date: datetime


class StudentsPut(StudentsPost):
    created_at: datetime
    updated_at: datetime


class StudentsPatch(BaseModel):
    name: Optional[str] = Field(example='Name')
    department: Optional[str] = Field(example='major')
    gender: Optional[str] = Field(example='gender')
    state: Optional[str] = Field(example='state')
    birth_date: Optional[datetime]


class StudentsResponse(BaseModel):
    id: UUID = Field(example=1234)
    name: str
    gender: str
    department: str
    state: str
    birth_date: datetime
    created_at: datetime
    updated_at: datetime


class AddressPost(BaseModel):
    email: str = Field(example='username@host.com', max_length=50)
    user_id: UUID


class AddressResponse(BaseModel):
    email_id: UUID = Field(example=1234)
    email: str
    user_id: UUID
