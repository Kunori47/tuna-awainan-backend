from fastapi import APIRouter, Header, UploadFile
from fastapi.responses import RedirectResponse
from models import *
from database import database
from typing import List
from controller.controller import *

router = APIRouter()

@router.get("/")
async def read_root():
    return RedirectResponse(url="/docs")

@router.get("/users", tags=["users"], response_model=list[User])
async def read_users():
    return UserController().getUser()

@router.delete("/delete-user", tags=["users"], response_model=dict)
async def delete_user(id: int):
    return UserController().deleteUser(id)

@router.put("/update-password", tags=["users"], response_model=dict)
async def update_user_password(id: int, password: str):
    return UserController().updateUserpassword(id, password)

@router.post("/signup", tags=["auth"], response_model=dict)
async def create_user(username: str, email: str, password: str):
    return UserController().create_user(username, email, password)

@router.post("/login", tags=["auth"], response_model=dict)
async def login_user(email: str, password: str):
    user = AuthController().login(email, password)
    token = AuthController().generate_token(user["id"])
    return {"message": "Login successful", "token": token}

@router.get("/roles", tags=["roles"], response_model=List[Role])
async def read_roles():
    database.execute("SELECT * FROM roles")
    roles = database.fetchall()
    roles_list = [{"id": role[0], "name_role": role[1]} for role in roles]
    return roles_list

@router.get("/tags", tags=["tags"], response_model=List[Tag])
async def read_tags():
    database.execute("SELECT * FROM tags")
    tags = database.fetchall()
    tags_list = [{"id": tag[0], "name": tag[1]} for tag in tags]
    return tags_list

@router.get("/specimens", tags=["specimens"], response_model=List[dict])
async def read_specimens():
    return SpecimensController().get_specimens()

@router.post("/create-specimen", tags=["specimens"], response_model=dict)
async def create_specimen(name: str, name_scientific: str, description: str, img: UploadFile):
    return SpecimensController().create_specimen(name, name_scientific, description, img)

@router.delete("/delete-specimen", tags=["specimens"], response_model=dict)
async def delete_specimen(id: int):
    return SpecimensController().delete_specimen(id)

@router.get("/post", tags=["post"], response_model=List[dict])
async def read_posts():
    return PostController().get_posts()

@router.post("/create-post", tags=["post"], response_model=dict)
async def create_post(title: str, content: str, id_user: int, img: UploadFile):
    return PostController().create_post(title, content, id_user, img)

@router.delete("/delete-post", tags=["post"], response_model=dict)
async def delete_post(id: int):
    return PostController().delete_post(id)

@router.get("/articles", tags=["articles"], response_model=List[dict])
async def read_articles():
    return ArticlesController().get_articles()

@router.post("/create-article", tags=["articles"], response_model=dict)
async def create_article(title: str, description: str, img: UploadFile, id_tag: int):
    return ArticlesController().create_article(title, description, id_tag, img)

@router.delete("/delete-article", tags=["articles"], response_model=dict)
async def delete_article(id: int):
    return ArticlesController().delete_article(id)

@router.get("/post/comments/{id_post}", tags=["post/comments"], response_model=CommentPost)
async def read_comments(id_post: int):
    return PostController().get_comments(id_post)

@router.post("/post/create-comments", tags=["post/comments"], response_model=dict)
async def create_comment(content: str, id_user: int, id_post: int):
    return PostController().create_comment(content, id_user, id_post)

@router.delete("/post/delete-comments", tags=["post/comments"], response_model=dict)
async def delete_comment(id: int):
    return PostController().delete_comment(id)

@router.get("/post/comments/answers/{id_comment}", tags=["post/comments/answers"], response_model=AnswerPost)
async def read_answers(id_comment: int):
    return PostController().get_answers(id_comment)

@router.post("/post/comments/create-answers", tags=["post/comments/answers"], response_model=dict)
async def create_answer(content: str, id_user: int, id_comment: int):
    return PostController().create_answer(content, id_user, id_comment)

@router.delete("/post/comments/delete-answers", tags=["post/comments/answers"], response_model=dict)
async def delete_answer(id: int):
    return PostController().delete_answer(id)

