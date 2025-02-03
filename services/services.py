import base64
import bcrypt
import jwt
import datetime
import os
from database import database, conn
from fastapi import UploadFile
from models import User
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

class PostService:
    def create_post(self, title: str, content: str, id_user: int, img: UploadFile):
        image_blob = img.file.read()

        database.execute("INSERT INTO post (title, content, id_user, img) VALUES (?, ?, ?, ?)",
                          (title, content, id_user, image_blob))
        conn.commit()
        return {"message": "Post created successfully"}
    
    def get_posts(self):
        database.execute("SELECT * FROM post")
        posts = database.fetchall()

        post_list = []
        for post in posts:
            img_base64 = base64.b64encode(post[4]).decode('utf-8') if post[4] else None
            post_dict = {
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "date_added": post[3],
                "img": img_base64,
                "id_user": post[5],
                
            }
            post_list.append(post_dict)
        
        return post_list
    
    def delete_post(self, id: int):
        database.execute("DELETE FROM post WHERE id = ?", (id,))
        conn.commit()
        return {"message": "Post deleted successfully"}
    
    def get_comments(self, id_post: int):
        database.execute("SELECT * FROM comment_post WHERE id_post = ?", (id_post,))
        comments = database.fetchall()
        comment_list = []
        for comment in comments:
            comment_dict = {
                "id": comment[0],
                "date_added": comment[1],
                "content": comment[2],
                "id_user": comment[3],
                "id_post": comment[4]
            }
            comment_list.append(comment_dict)
        return comment_list
    
    def create_comment(self, content: str, id_user: int, id_post: int):
        database.execute("INSERT INTO commentpost (content, id_user, id_post) VALUES (?, ?, ?)",
                          (content, id_user, id_post))
        conn.commit()
        return {"message": "Comment created successfully"}
    
    def delete_comment(self, id: int):
        database.execute("DELETE FROM commentpost WHERE id = ?", (id,))
        conn.commit()
        return {"message": "Comment deleted successfully"}
    
    def get_answers(self, id_comment: int):
        database.execute("SELECT * FROM answer_comment WHERE id_comment = ?", (id_comment,))
        answers = database.fetchall()
        answer_list = []
        for answer in answers:
            answer_dict = {
                "id": answer[0],
                "date_added": answer[1],
                "content": answer[2],
                "id_user": answer[3],
                "id_comment": answer[4]
            }
            answer_list.append(answer_dict)
        
        return answer_list
    
    def create_answer(self, content: str, id_user: int, id_comment: int):
        database.execute("INSERT INTO answerpost (content, id_user, id_comment) VALUES (?, ?, ?)",
                         (content, id_user, id_comment))
        conn.commit()
        return {"message": "Answer created successfully"}
    
    def delete_answer(self, id: int):
        database.execute("DELETE FROM answerpost WHERE id = ?", (id,))
        conn.commit()
        return {"message": "Answer deleted successfully"}

class UserService:

    def email_exists(self, email: str) -> bool:
        database.execute("SELECT COUNT(*) FROM profiles WHERE email = ?", (email,))
        count = database.fetchone()[0]
        return count > 0

    def username_exists(self, username: str) -> bool:
        database.execute("SELECT COUNT(*) FROM profiles WHERE username = ?", (username,))
        count = database.fetchone()[0]
        return count > 0
    
    def createUser(self, username: str, email: str, password: str,):
        
        if self.email_exists(email):
            raise ValueError("El email ya está registrado")
        if self.username_exists(username):
            raise ValueError("El nombre de usuario ya está registrado")
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        database.execute("INSERT INTO profiles (username, email, password) VALUES (?, ?, ?)", 
                         (username, email, hashed_password)
                        )
        conn.commit()
        return {"message": "User created successfully"}

    def getUser(self):
        database.execute("SELECT * FROM profiles")
        users = database.fetchall()
        return [User(id=user[0], username=user[1], email=user[2], password=user[3], id_role=user[4]) for user in users]
    
    def deleteUser(self, id: int):
        database.execute("DELETE FROM profiles WHERE id = ?", (id,))
        conn.commit()
        return {"message": "User deleted successfully"}
    
    def updateUserpassword(self, id: int, password: str):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        database.execute("UPDATE profiles SET password = ? WHERE id = ?", (hashed_password, id))
        conn.commit()
        return {"message": "Password updated successfully"}

class AuthService:
    def __init__(self):
        self.revoked_tokens = set()

    def generate_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.now() + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    #def logout(self, token: str):
    #    self.revoked_tokens.add(token)
    #    return {"message": "Logout successful"}

    #def is_token_revoked(self, token: str) -> bool:
    #    return token in self.revoked_tokens

    def login(self, email: str, password: str):
        database.execute("SELECT * FROM profiles WHERE email = ?", (email,))
        user = database.fetchone()
        if user:
            if self.verify_password(password, user[3]):
                return {"id": user[0], "username": user[1], "email": user[2]}
            else:
                return {"message": "Incorrect password"}
        else:
            return {"message": "User not found"}
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))   

class ArticlesService:
    def get_articles(self):
        database.execute("SELECT * FROM articles")
        articles = database.fetchall()

        article_list = []
        for article in articles:
            img_base64 = base64.b64encode(article[4]).decode('utf-8') if article[4] else None
            article_dict = {
                "id": article[0],
                "title": article[1],
                "description": article[2],
                "date_added": article[3],
                "img": img_base64,
                "id_tag": article[5]
            }
            article_list.append(article_dict)
        return article_list
    
    
    def create_article(self, title: str, description: str, id_tag: int, img: UploadFile):
        image_blob = img.file.read()

        database.execute("INSERT INTO articles (title, description, img, id_tag) VALUES (?, ?, ?, ?)",
                          (title, description, image_blob, id_tag))
        conn.commit()
        return {"message": "Article created successfully"}
    
    def delete_article(self, id: int):
        database.execute("DELETE FROM articles WHERE id = ?", (id,))
        conn.commit()
        return {"message": "Article deleted successfully"}
    
class SpecimensService:
    def get_specimens(self):
        database.execute("SELECT * FROM specimens")
        specimens = database.fetchall()
        specimen_list = []
        for specimen in specimens:
            img_base64 = base64.b64encode(specimen[4]).decode('utf-8') if specimen[4] else None
            specimen_dict = {
                "id": specimen[0],
                "name": specimen[1],
                "name_scientific": specimen[2],
                "description": specimen[3],
                "img": img_base64
            }
            specimen_list.append(specimen_dict)
        return specimen_list
    
    def create_specimen(self, name: str, name_scientific: str, description: str, img: UploadFile):
        image_blob = img.file.read()

        database.execute("INSERT INTO specimens (name, name_scientific, description, img) VALUES (?, ?, ?, ?)",
                          (name, name_scientific, description, image_blob))
        conn.commit()
        return {"message": "Specimen created successfully"}
    
    def delete_specimen(self, id: int):
        database.execute("DELETE FROM specimens WHERE id = ?", (id,))
        conn.commit()
        return {"message": "Specimen deleted successfully"}
    