import datetime
from typing import Optional
from uuid import uuid4
from uuid import UUID
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from db import engine
from modules import Gender, NewStudents, NewStudents_Patch, TestDB
from session import JSONResponse
from db import students as student_table

app = FastAPI()
###

Students = {"1": {'name': 'ghaid', 'major': 'CS', "gender": "female"},
            "2": {'name': 'khalid', 'major': 'CiS', "gender": "male"},
            "3": {'name': 'lina', 'major': 'CS', "gender": "female"},
            "4": {'name': 'ahmad', 'major': 'CS', "gender": "male"}}


def data_input(id: str, student: NewStudents) -> dict:
    Students[id] = {"name": student.name,
                    "major": student.major,
                    "gender": student.gender}
    return student

##


@app.get("/getstudentbyid/{id}")
def get_student_by_id(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        student = conn.execute(student_table.select().where(
            student_table.c.id == id)).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Student with id: {id} dose not exist'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': TestDB(**student._asdict())}
    )


@app.post("/addstudent")
def add_student(student: NewStudents) -> JSONResponse:
    with engine.begin() as conn:
        new_student = conn.execute(student_table.insert().returning(
            student_table).values(**student.dict(exclude_none=True)))
        if not new_student:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='BAD DATA'
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'data': new_student.first()}
        )


@app.delete("/students/{id}")
def delete_student(id: str):
    with engine.connect() as conn:
        stmt = student_table.delete().where(student_table.c.id == id)
        conn.execute(stmt)


@app.get("/students")
def get_student(gender: Optional[str] = None, department: Optional[str] = None) -> JSONResponse:

    if gender and not department:
        with engine.connect() as conn:
            students = conn.execute(student_table.select().where(
                student_table.c.gender == gender)).fetchall()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=(TestDB(**student._asdict()) for student in students)
        )
    if not gender and department:
        with engine.connect() as conn:
            students = conn.execute(student_table.select().where(
                student_table.c.department == department)).fetchall()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=(TestDB(**student._asdict()) for student in students)
        )
    if gender and department:
        with engine.connect() as conn:
            students = conn.execute(student_table.select().where(
                student_table.c.department == department, student_table.c.gender == gender)).fetchall()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=(TestDB(**student._asdict()) for student in students)
        )
    else:
        with engine.connect() as conn:
            students = conn.execute(student_table.select().fetchall())
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=(TestDB(**student._asdict())
                         for student in students)
            )


@app.put("/putstudent/{id}")
def put_student(student: NewStudents, id) -> JSONResponse:
    try:
        with engine.begin() as conn:
            updated_student = conn.execute(student_table.update().returning(student_table).where(
                student_table.c.id == id).values(**student.dict(exclude_none=True), ))
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'data': updated_student.first()}
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='BAD DATA '
        )


@app.patch("/patchstudent/{id}")
def update_student(student: NewStudents_Patch, id) -> JSONResponse:
    try:
        with engine.begin() as conn:
            new_student = conn.execute(student_table.update().returning(student_table).where(
                student_table.c.id == id).values(**student.dict(exclude_none=True)))
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'data': new_student.first()}
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='AN ERROR CAME UP '
        )
