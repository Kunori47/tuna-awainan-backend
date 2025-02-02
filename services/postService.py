import base64
from database import database, conn
from fastapi import UploadFile
from models import Post, CommentPost, AnswerPost

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
                "id_user": post[3],
                "img": img_base64
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
    
    
        
    
    