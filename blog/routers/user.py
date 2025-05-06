from fastapi import APIRouter, Depends, status
from .. import schemas, database
from typing import List
from sqlalchemy.orm import Session
from ..repository import user_repository as repository

get_db = database.get_db

router = APIRouter(prefix="/user", tags=["Users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ShowUser],
)
def get_all(db: Session = Depends(get_db)):
    return repository.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.User, db: Session = Depends(get_db)):
    return repository.create(request, db)


@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=schemas.ShowUser)
def show(id: int, db: Session = Depends(get_db)):
    return repository.show(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User, db: Session = Depends(get_db)):
    return repository.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return repository.destroy(id, db)
