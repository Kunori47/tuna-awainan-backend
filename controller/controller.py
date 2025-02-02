from services.services import *
from fastapi import UploadFile, HTTPException, Header


class PostController:
    def __init__(self):
        self.postService = PostService()
    
    def create_post(self, title: str, content: str, id_user: int, img: UploadFile):
        return self.postService.create_post(title, content, id_user, img)
    
    def get_posts(self):
        return self.postService.get_posts()
    
    def delete_post(self, id: int):
        return self.postService.delete_post(id)
    
    def get_comments(self, id_post: int):
        return self.postService.get_comments(id_post)
    
    def create_comment(self, content: str, id_user: int, id_post: int):
        return self.postService.create_comment(content, id_user, id_post)
    
    def delete_comment(self, id: int):
        return self.postService.delete_comment(id)
    
    def get_answers(self, id_comment: int):
        return self.postService.get_answers(id_comment)
    
    def create_answer(self, content: str, id_user: int, id_comment: int):
        return self.postService.create_answer(content, id_user, id_comment)
    
    def delete_answer(self, id: int):
        return self.postService.delete_answer(id)


class UserController:
    def __init__(self):
        self.userService = UserService()

    def create_user(self, username: str, email: str, password: str):
        try:
            if not (8 <= len(password) <= 30):
                raise ValueError("La contraseña debe tener entre 8 y 30 caracteres")
            return self.userService.createUser(username, email, password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def getUser(self):
        return self.userService.getUser()
    
    def deleteUser(self, id: int):
        return self.userService.deleteUser(id)
    
    def updateUserpassword(self, id: int, password: str):
        return self.userService.updateUserpassword(id, password)
    
class AuthController:
    def __init__(self):
        self.authService = AuthService()

    
    #def logout(self, token: str):
    #    return self.authService.logout(token) 
    
    def generate_token(self, user_id: int):
        return self.authService.generate_token(user_id)    
    
    def login(self, email: str, password: str):
        return self.authService.login(email, password)
    
    
class ArticlesController:
    def __init__(self):
        self.articlesService = ArticlesService()
    
    def get_articles(self):
        return self.articlesService.get_articles()
    
    def create_article(self, title: str, description: str, id_tag: int, img: UploadFile):
        return self.articlesService.create_article(title, description, id_tag, img)
    
    def delete_article(self, id: int):
        return self.articlesService.delete_article(id)
    
class SpecimensController:
    def __init__(self):
        self.specimensService = SpecimensService()

    def get_specimens(self):
        return self.specimensService.get_specimens()
    
    def create_specimen(self, name: str, name_scientific: str, description: str, img: UploadFile):
        return self.specimensService.create_specimen(name, name_scientific, description, img)
    
    def delete_specimen(self, id: int):
        return self.specimensService.delete_specimen(id)