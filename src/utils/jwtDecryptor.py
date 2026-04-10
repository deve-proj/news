import jwt
from dotenv import load_dotenv
import os

load_dotenv()

class JWTDecryptor:

    def __init__(self, auth):
        
        self.token = auth.split(" ")[1] if "Bearer" in auth.split(" ") else False


    def extract_user_id(self):

        return jwt.decode(self.token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"], options={"verify_exp": False})["sub"]