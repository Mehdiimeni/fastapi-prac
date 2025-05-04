from fastapi import FastAPI
from . import schemas
from . import schemas, models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.post("/blog")
def create_blog(blog: schemas.Blog):
    return {"data": f"Blog is created with {blog.title} and {blog.body}"}