from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()

get_db = database.get_db


@router.get("/blog",
            response_model=List[schemas.ShowBlog],
            status_code=status.HTTP_200_OK,
            tags=["blogs"])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/blog/{id}",
               status_code=status.HTTP_204_NO_CONTENT,
               tags=["blogs"])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    db.delete(blog)
    db.commit()
    return  # 204 No Content should not return a body


@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update_blog(id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    blog_to_update.title = blog.title
    blog_to_update.body = blog.body
    db.commit()
    return "blog_to_update"


@router.get("/blog/{id}",
            status_code=status.HTTP_200_OK,
            response_model=schemas.ShowBlog,
            tags=["blogs"])
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    return blog
