from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def index():
    return {"data": {'name': 'Index page'}}

@app.get("/about")
def about():
    return {"data": {'name': 'About page'}}