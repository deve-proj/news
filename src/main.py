from fastapi import FastAPI, Header, UploadFile, File, Form, HTTPException, status
from .database.main import DataBase
from .models.post import post_model
from .common.jwtDecryptor import JWTDecryptor
from typing import Optional
from .redisClient.main import RedisClient
from .s3.main import MinioClient
from typing import List, Optional
import json
from fastapi.middleware.cors import CORSMiddleware
from .graphql.main import graphql_router

app = FastAPI(title="DEVE news center", version='0.0.1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dataBase = DataBase()
redisClient = RedisClient()
s3 = MinioClient()

app.include_router(graphql_router, prefix="")

@app.post('/news')
async def create_post(structure : str = Form(...), files : Optional[List[UploadFile]] = None, auth : Optional[str] = Header(None, alias="Authorization")):

    jwt = JWTDecryptor(auth)

    try:

        structure = post_model.model_validate(json.loads(structure))

        post_id = await dataBase.create_post(structure, jwt.extract_user_id())

        for file in files:

            await s3.upload_file(post_id, file, file.filename)


    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))

@app.delete('/news', status_code=status.HTTP_200_OK, operation_id="deletePost")
async def delete_post(post_id : str, auth : Optional[str] = Header(None, alias="Authorization")):

    jwt = JWTDecryptor(auth)

    return await dataBase.delete_post(post_id, jwt.extract_user_id())

@app.put('/news', status_code=status.HTTP_201_CREATED, operation_id="updatePost")
async def update_post(post_id : str, post_data : post_model, auth : Optional[str] = Header(None, alias="Authorization")):

    jwt = JWTDecryptor(auth)

    return await dataBase.update_post(post_id, jwt.extract_user_id(), post_data)

@app.get("/test", operation_id="tester")
async def test(structure : str = Form(...), files : List[UploadFile] = File(...)):

    try:

        post_data = post_model.model_validate(json.loads(structure))

        s3.upload_file(post_data.p)

    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))