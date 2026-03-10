from fastapi import FastAPI, Header, UploadFile, File, Form, HTTPException
from .database.main import DataBase
from .models.createPost import create_post_model
from .common.jwtDecryptor import JWTDecryptor
from typing import Optional
from .redisClient.main import RedisClient
from .s3.main import MinioClient
from typing import List
import json
from .common.jsonParser import replace_image_name_to_url_in_post

app = FastAPI()
dataBase = DataBase()
redisClient = RedisClient()
s3 = MinioClient()

@app.get('/news')
async def get_news_by_author_id(user_id : str = None, post_id : str = None):

    if post_id:

        await dataBase.update_views_counter_by_post_id(post_id)

        return await dataBase.get_post_by_post_id(post_id)

    if user_id:

        return await dataBase.get_posts_by_user_id(user_id)

    else:

        return {"result": await dataBase.get_all_posts(), "time": 2434}

@app.post('/news')
async def create_post(structure : str = Form(...), files : List[UploadFile] = File(...), auth : Optional[str] = Header(None, alias="Authorization")):

    jwt = JWTDecryptor(auth)

    try:

        structure = create_post_model.model_validate(json.loads(structure))

        post_id = await dataBase.create_post(structure, jwt.extract_user_id())

        for file in files:

            await s3.upload_file(post_id, file, file.filename)


    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))

@app.delete('/news')
async def delete_post(post_id : str, auth : Optional[str] = Header(None, alias="Authorization")):

    jwt = JWTDecryptor(auth)

    return await dataBase.delete_post(post_id, jwt.extract_user_id())

@app.put('/news')
async def update_post(post_id : str, post_data : create_post_model, auth : Optional[str] = Header(None, alias="Authorization")):

    jwt = JWTDecryptor(auth)

    return await dataBase.update_post(post_id, jwt.extract_user_id(), post_data)

@app.get("/test")
async def test(structure : str = Form(...), files : List[UploadFile] = File(...)):

    try:

        post_data = create_post_model.model_validate(json.loads(structure))

        s3.upload_file(post_data.p)

    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))