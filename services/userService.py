import bcrypt
from database import database, conn
from models import User

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
    
    def loginUser(self, email: str, password: str):
        database.execute("SELECT * FROM profiles WHERE email = ?", (email,))
        user = database.fetchone()
        if user:
            if self.verify_password(password, user[3]):
                return {"message": "Login successful"}
            else:
                return {"message": "Incorrect password"}
        else:
            return {"message": "User not found"}
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def getUser(self):
        database.execute("SELECT * FROM profiles")
        users = database.fetchall()
        return [User(id=user[0], username=user[1], email=user[2], password=user[3], id_role=user[4]) for user in users]   


