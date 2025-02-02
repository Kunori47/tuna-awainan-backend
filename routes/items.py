from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from models import *
from database import database
from typing import List
from controller.userController import UserController
from controller.postController import PostController



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

@router.get("/post", tags=["post"], response_model=List[dict])
def read_posts():
    return PostController().get_posts()

@router.post("/create-post", tags=["post"], response_model=dict)
def create_post(title: str, content: str, id_user: int, img: UploadFile):
    return PostController().create_post(title, content, id_user, img)

@router.delete("/delete-post", tags=["post"], response_model=dict)
def delete_post(id: int):
    return PostController().delete_post(id)

@router.get("/articles", tags=["articles"], response_model=Article)
def read_articles():
    database.execute("SELECT * FROM articles")
    articles = database.fetchall()
    return articles

@router.get("/post/comments/{id_post}", tags=["post/comments"], response_model=CommentPost)
def read_comments(id_post: int):
    return PostController().get_comments(id_post)

@router.post("/post/create-comments", tags=["post/comments"], response_model=dict)
def create_comment(content: str, id_user: int, id_post: int):
    return PostController().create_comment(content, id_user, id_post)

@router.delete("/post/delete-comments", tags=["post/comments"], response_model=dict)
def delete_comment(id: int):
    return PostController().delete_comment(id)

@router.get("/post/answers", tags=["post/answers"], response_model=AnswerPost)
def read_answers(id_comment: int):
    return PostController().get_answers(id_comment)

@router.post("/post/create-answers", tags=["post/answers"], response_model=dict)
def create_answer(content: str, id_user: int, id_comment: int):
    return PostController().create_answer(content, id_user, id_comment)

@router.delete("/post/delete-answers", tags=["post/answers"], response_model=dict)
def delete_answer(id: int):
    return PostController().delete_answer(id)

