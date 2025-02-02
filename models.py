from fastapi import UploadFile, File
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(..., example=1)
    username: str = Field(..., example="John Doe")
    email: str = Field(..., example="elpapu@gmail.com")
    password: str = Field(..., example="$2b$12$KIXaRzpUvuX8J.0iN/7bqeC/poFiyHwaQPjkF3gUoqQja99x.L/Au")
    id_role: int = Field(..., example=1)

class Role(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Administrador")

class Tag(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Conservacion del agua")

class Specimen(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="Pez")
    name_scientific: str = Field(..., example="Pisces")
    description: str = Field(..., example="Pez de agua dulce")
    img: str = Field(..., example="pez.jpg")

class Post(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="El agua y su importancia")
    content: str = Field(..., example="El agua es un recurso natural vital para la vida")
    date_added: str = Field(..., example="2021-09-01")
    img: UploadFile = File(...)
    id_user: int = Field(..., example=1)

class Article(BaseModel):
    id: int = Field(..., example=1)
    title: str = Field(..., example="El agua y su importancia")
    description: str = Field(..., example="El agua es un recurso natural vital para la vida")
    date_added: str = Field(..., example="2021-09-01")
    img: str = Field(..., example="agua.jpg")
    id_tag: int = Field(..., example=1)

class CommentPost(BaseModel):
    id: int = Field(..., example=1)
    date_added: str = Field(..., example="2021-09-01")
    content: str = Field(..., example="Excelente articulo")
    id_user: int = Field(..., example=1)
    id_post: int = Field(..., example=1)

class AnswerPost(BaseModel):
    id: int = Field(..., example=1)
    date_added: str = Field(..., example="2021-09-01")
    content: str = Field(..., example="Gracias por el comentario")
    id_user: int = Field(..., example=1)
    id_comment: int = Field(..., example=1)
    
    
    
