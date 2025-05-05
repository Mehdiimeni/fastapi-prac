from fastapi import FastAPI, Depends, status,HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session  
from typing import List
from .hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED,tags=["blogs"])
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit() 
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT,tags=["blogs"])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )
    db.delete(blog)
    db.commit()
    return  # 204 No Content should not return a body


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])
def update_blog(id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )
    blog_to_update.title = blog.title
    blog_to_update.body = blog.body
    db.commit()
    return "blog_to_update"
         

@app.get("/blog",response_model=List[schemas.ShowBlog],status_code=status.HTTP_200_OK,tags=["blogs"])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog,tags=["blogs"])
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )
    return blog



@app.post("/user", status_code=status.HTTP_201_CREATED,tags=["users"])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(user.password)
    new_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 


@app.get("/user", status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser],tags=["users"])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser,tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    return user    


@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT,tags=["users"])
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not  user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    db.delete(user)
    db.commit()
    return  "user deleted"

@app.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED,tags=["users"])
def update_user(id: int, user: schemas.User, db: Session = Depends(get_db)):
    user_to_update = db.query(models.User).filter(models.User.id == id).first()
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    user_to_update.email = user.email
    user_to_update.name = user.name
    db.commit()
    return "user successful updated"    