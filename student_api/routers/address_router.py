from uuid import UUID
from fastapi import APIRouter, HTTPException
from db import engine, addresses
from fastapi import HTTPException, status
from modules import AddressResponse, AddressPost
from session import JSONResponse
from sqlalchemy.exc import IntegrityError, IntegrityError

router = APIRouter()

router = APIRouter(
    prefix="/addresses",
    tags=["adresses"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get('/', tags=["adresses"])
def get_all_address() -> JSONResponse:
    with engine.connect() as conn:
        address_data = conn.execute(addresses.select()).first()
        print('>>>>>', address_data)
    if not address_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'email address  with id: {id} dose not exist'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': AddressResponse(**address_data._asdict())}
    )


@router.post('/', response_model=AddressResponse, tags=["adresses"])
def add_address(email_address: AddressPost):
    try:
        with engine.begin() as conn:
            new_address = conn.execute(addresses.insert().returning(
                addresses).values(**email_address.dict()))
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Bad data')

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'data': new_address.first()}
    )


@router.get('/{id}', tags=["adresses"])
def get_email_address_by_id(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        email_address_data = conn.execute(addresses.select().where(
            addresses.c.email_id == id)).first()
        return AddressResponse(**email_address_data._asdict())


@router.delete('/{id}', tags=["adresses"])
def delete_email_address(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        email_address_deleted = conn.execute(
            addresses.delete().where(addresses.c.email_id == id)).rowcount

    if not email_address_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'email address  with id: {id} dose not exist'
        )

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT
    )
