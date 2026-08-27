from datetime import date

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from schemas import PostCreate, PostResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

posts = [
    {
        "id": 1,
        "title": "Getting Started with FastAPI",
        "content": "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python.",
        "author": "Sachin Prasad",
        "date_posted": "2026-01-05",
    },
    {
        "id": 2,
        "title": "Asynchronous Programming in Python",
        "content": "Learn how async and await help handle thousands of concurrent requests efficiently.",
        "author": "Jane Doe",
        "date_posted": "2026-01-10",
    },
    {
        "id": 3,
        "title": "Mastering Jinja2 Templates",
        "content": "Render dynamic HTML web pages smoothly in your FastAPI applications using Jinja2.",
        "author": "Alex Smith",
        "date_posted": "2026-01-15",
    },
]


@app.get("/", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return posts


@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):

    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found"
    )


@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": str(date.today()),
    }
    posts.append(new_post)
    return new_post


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exc: StarletteHTTPException):
    message = (
        exc.detail
        if exc.detail
        else "An Error Occured. Please check your  request and try again."
    )
    return JSONResponse(
        status_code=exc.status_code, content={"detail": message}
    )


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )
