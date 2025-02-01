from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from models import *
from database import database
from controller.userController import UserController


router = APIRouter()

@router.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@router.get("/users", tags=["users"], response_model=list[User])
def read_users():
    return UserController().getUser()

@router.post("/signup", tags=["users"], response_model=dict)
def create_user(username: str, email: str, password: str):
    return UserController().create_user(username, email, password)

@router.post("/login", tags=["users"], response_model=dict)
def login_user(email: str, password: str):
    return UserController().login_user(email, password)

@router.get("/roles", tags=["roles"], response_model=Role)
def read_roles():
    database.execute("SELECT * FROM roles")
    roles = database.fetchall()
    return roles

@router.get("/tags", tags=["tags"], response_model=Tag)
def read_tags():
    database.execute("SELECT * FROM tags")
    tags = database.fetchall()
    return tags

@router.get("/specimens", tags=["specimens"], response_model=Specimen)
def read_specimens():
    database.execute("SELECT * FROM specimens")
    specimens = database.fetchall()
    return specimens

@router.get("/post", tags=["post"], response_model=Post)
def read_posts():
    database.execute("SELECT * FROM post")
    posts = database.fetchall()
    return posts

@router.get("/articles", tags=["articles"], response_model=Article)
def read_articles():
    database.execute("SELECT * FROM articles")
    articles = database.fetchall()
    return articles

@router.get("/post/comments", tags=["post/comments"], response_model=CommentPost)
def read_comments():
    database.execute("SELECT * FROM commentpost")
    comments = database.fetchall()
    return comments

@router.get("/post/answers", tags=["post/answers"], response_model=AnswerPost)
def read_answers():
    database.execute("SELECT * FROM answerpost")
    answers = database.fetchall()
    return answers
