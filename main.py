from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

posts = [
    {
        "id": 1,
        "title": "Getting Started with FastAPI",
        "content": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python.",
        "author": "Sachin Prasad",
        "date_posted": "2026-01-05"
    },
    {
        "id": 2,
        "title": "Asynchronous Programming in Python",
        "content": "Learn how async and await help handle thousands of concurrent requests efficiently.",
        "author": "Jane Doe",
        "date_posted": "2026-01-10"
    },
    {
        "id": 3,
        "title": "Mastering Jinja2 Templates",
        "content": "Render dynamic HTML web pages smoothly in your FastAPI applications using Jinja2.",
        "author": "Alex Smith",
        "date_posted": "2026-01-15"
    },
]


@app.get("/", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts,"title":"Home"})


@app.get("/posts")
def get_posts():
    return posts
