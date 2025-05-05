from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database, hashing
from typing import List
from sqlalchemy.orm import Session

get_db = database.get_db
Hash = hashing.Hash()

router = APIRouter()


@router.post("/user", status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(user.password)
    new_user = models.User(name=user.name,
                           email=user.email,
                           password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user",
            status_code=status.HTTP_200_OK,
            response_model=List[schemas.ShowUser],
            tags=["users"])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/user/{id}",
            status_code=status.HTTP_200_OK,
            response_model=schemas.ShowUser,
            tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    return user


@router.delete("/user/{id}",
               status_code=status.HTTP_204_NO_CONTENT,
               tags=["users"])
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    db.delete(user)
    db.commit()
    return "user deleted"


@router.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["users"])
def update_user(id: int, user: schemas.User, db: Session = Depends(get_db)):
    user_to_update = db.query(models.User).filter(models.User.id == id).first()
    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    user_to_update.email = user.email
    user_to_update.name = user.name
    db.commit()
    return "user successful updated"
