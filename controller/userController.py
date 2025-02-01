from fastapi import HTTPException
from services.userService import UserService

class UserController:
    def __init__(self):
        self.userService = UserService()

    def create_user(self, username: str, email: str, password: str):
        try:
            return self.userService.createUser(username, email, password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def login_user(self, email: str, password: str):
        return self.userService.loginUser(email, password)

    def getUser(self):
        return self.userService.getUser()