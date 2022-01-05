from typing import Optional
from uuid import UUID

from db import engine, students
from fastapi import FastAPI, HTTPException, status
from modules import StudentsPatch, StudentsPost, StudentsPut, StudentsResponse
from session import JSONResponse
from sqlalchemy.exc import IntegrityError

app = FastAPI()


@app.get('/students/{id}')
def get_student_by_id(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        student_data = conn.execute(students.select().where(
            students.c.id == id)).first()
    if not student_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Student with id: {id} dose not exist'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': StudentsResponse(**student_data._asdict())}
    )


@app.post('/student', response_model=StudentsResponse)
def add_student(student: StudentsPost) -> JSONResponse:
    try:
        with engine.begin() as conn:
            new_student = conn.execute(students.insert().returning(
                students).values(**student.dict()))
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bad data')

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': new_student.first()}
    )


@app.delete('/students/{id}')
def delete_student(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        student_deleted = conn.execute(
            students.delete().where(students.c.id == id)).rowcount

    if not student_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Student with id: {id} dose not exist'
        )

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT
    )


@app.get('/students', response_model=StudentsResponse)
def get_student(gender: Optional[str] = None,
                department: Optional[str] = None) -> JSONResponse:
    sel = None
    if gender and not department:
        sel = students.select().where(students.c.gender == gender)

    elif not gender and department:
        sel = students.select().where(students.c.department == department)

    elif gender and department:
        sel = students.select()\
            .where(students.c.department == department)\
            .where(students.c.gender == gender)

    else:
        sel = students.select()

    with engine.connect() as conn:
        student_data = conn.execute(sel).fetchall()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': (StudentsResponse(**student._asdict())
                 for student in student_data)}
    )


@app.put("/student/{id}", response_model=StudentsResponse)
def put_student(student: StudentsPut, student_id: UUID) -> JSONResponse:
    with engine.begin() as conn:
        deleted_student = conn.execute(students.delete().where(
            students.c.id == student_id
        )).rowcount

        new_student = conn.execute(
            students.insert().values(id=student_id,
                                     ** student.dict()).returning(students))

        if deleted_student:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={
                            'data': StudentsResponse(**new_student.first())
                        })


@app.patch("/student/{id}", response_model=StudentsResponse)
def update_student(student: StudentsPatch, student_id: UUID) -> JSONResponse:
    with engine.begin() as conn:
        updated_student = conn.execute(students.update().where(
            students.c.id == student_id)
            .values(**student.dict(exclude_none=True)).returning(students))

        if not updated_student.rowcount:
            raise HTTPException(
                status_code=404,
                detail=f'Student with id: ({student_id}) dose not exist'
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'data': updated_student.first()}
        )
