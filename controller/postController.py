from services.postService import PostService
from fastapi import UploadFile

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
    
    