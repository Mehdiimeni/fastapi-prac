from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def index():
    return {"data": 'Index page'}

@app.get("/about")
def about():
    return {"data":'About page'}


@app.get("/blog")
def all_blogs(limit:int=10,published:bool=True, sort: Optional[str]=None):
    
    if published:
        return {"data": f'All {limit} published blogs from the database'}
    else:
        return {"data": f'Blog page unpublished limit : {limit} '}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}

@app.get("/blog/{id}")
def show(id:int):
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id:int,limit:int=10):
    return {"data": f'{id} , {limit}'}


# Post part

class Blog(BaseModel):
    pass

@app.post("/blog")
def create_blog(request: Blog):
    return {"data": "Blog created"}