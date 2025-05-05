from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog_repository as repository

router = APIRouter(prefix="/blog", tags=["Blogs"])

get_db = database.get_db


@router.get("/",
            response_model=List[schemas.ShowBlog],
            status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db)):
    return repository.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return repository.create(request, db)


@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    return repository.show(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return repository.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return repository.destroy(id, db)
