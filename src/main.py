from fastapi import FastAPI, Header
from .database.main import DataBase
from .models.createPost import create_post_model
from .common.jwtDecryptor import JWTDecryptor
from typing import Optional

app = FastAPI()
dataBase = DataBase()

@app.get('/news')
async def get_news_by_author_id(user_id : str = None, post_id : str = None, auth : Optional[str] = Header(None, alias="Authorization")):

    if post_id:

        return await dataBase.get_post_by_post_id(post_id)

    if user_id:

        return await dataBase.get_posts_by_user_id(user_id)

    else:

        return await dataBase.get_all_posts()

@app.post('/news')
async def create_post(post_data : create_post_model, auth : Optional[str] = Header(None, alias="Authorization")):

    jwt = JWTDecryptor(auth)

    return await dataBase.create_post(post_data, jwt.extract_user_id())

@app.delete('/news')
async def delete_post(post_id : str, auth : Optional[str] = Header(None, alias="Authorization")):

    jwt = JWTDecryptor(auth)

    return await dataBase.delete_post(post_id, jwt.extract_user_id())

@app.put('/news')
async def update_post(post_id : str, post_data : create_post_model, auth : Optional[str] = Header(None, alias="Authorization")):

    jwt = JWTDecryptor(auth)

    return await dataBase.update_post(post_id, jwt.extract_user_id(), post_data)