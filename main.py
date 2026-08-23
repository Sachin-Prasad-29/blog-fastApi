from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()

posts = [{"name" : "post 1" },{"name" : "post 2" },{"name" : "post 3" } ]


@app.get("/",response_class=HTMLResponse,include_in_schema=False)
def home():
    return "<h1>Welcome to Blog Fastapi</h1>"

@app.get("/posts")
def get_posts():
    return posts
