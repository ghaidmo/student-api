from fastapi import Header, HTTPException


async def get_token_header(password: str = Header(...)):
    if password != "secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(user_name: str):
    if user_name != "ghaid":
        raise HTTPException(
            status_code=400, detail="wrong username")
