
from fastapi import FastAPI, Depends, FastAPI
from .routers import student_router, address_router
from.dependencies import get_query_token, get_token_header


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
app.include_router(student_router.router)
app.include_router(address_router.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
