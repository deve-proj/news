from fastapi import FastAPI, Header, UploadFile, File, Form, HTTPException, status, Body
from .database.database import DataBase
from .models.post_model import post_model
from .utils.jwtDecryptor import JWTDecryptor
from typing import Optional
from .clients.redis.redisClient import RedisClient
from .clients.minio.minioClient import MinioClient
from typing import List, Optional
import json
from fastapi.middleware.cors import CORSMiddleware
from .graphql.graphql import graphql_router
from .models.comment_model import comment_model
from .utils.decorators.require_post_owner import require_post_owner
from .clients.backend.backendClient import BackendClient

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
backend = BackendClient()

app.include_router(graphql_router, prefix="")

@app.post('/news')
async def create_post(post_data : str = Form(...), files : Optional[List[UploadFile]] = None, auth : Optional[str] = Header(None, alias="Authorization")):

    try:

        jwt = JWTDecryptor(auth)

        post_data = post_model.model_validate(json.loads(post_data))

        post_id = await dataBase.create_post(post_data, jwt.extract_user_id())

        for file in files:

            await s3.upload_file(post_id, file, file.filename)

    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))


@app.delete('/news', status_code=status.HTTP_200_OK, operation_id="deletePost")
@require_post_owner()
async def delete_post(post_id : str, auth : Optional[str] = Header(None, alias="Authorization")):

    await s3.delete_post_files(post_id)
    await dataBase.delete_post(post_id)


@app.put('/news', status_code=status.HTTP_201_CREATED, operation_id="updatePost")
@require_post_owner()
async def update_post(post_id : str = Form(...), post_data : str = Form(...), files : Optional[List[UploadFile]] = None, auth : Optional[str] = Header(None, alias="Authorization")):
    
    post_data = post_model.model_validate(json.loads(post_data))
    
    await s3.delete_post_files(post_id)

    for file in files:

            await s3.upload_file(post_id, file, file.filename)

    return await dataBase.update_post(post_id, post_data)

@app.post('/news/comment')
async def comment(comment : comment_model = Body(...), auth : Optional[str] = Header(None, alias="Authorization")):

    try:

        # jwt = JWTDecryptor(auth)

        comment = comment_model.model_dump(comment)

        await dataBase.add_comment(comment['post_id'], comment)

    except Exception as e:

        return HTTPException(status_code=400, detail=str(e))
    
@app.post('/news/comment/reply')
async def reply(reply : comment_model = Body(...), auth : Optional[str] = Header(None, alias="Authorization")):

    try:

        # jwt = JWTDecryptor(auth)

        reply = comment_model.model_dump(reply)

        await dataBase.reply_to_comment(reply['parent_id'], reply)

    except Exception as e:

        return HTTPException(status_code=400, detail=str(e))

@app.post('/news/comment/like')
async def like(comment_id : str, auth : Optional[str] = Header(None, alias="Authorization")):

    try:

        return await dataBase.like_comment(comment_id)

    except Exception as e:

        return HTTPException(status_code=400, detail=str(e))
    
@app.post('/news/comment/dislike')
async def dislike(comment_id : str, auth : Optional[str] = Header(None, alias="Authorization")):

    try:

        return await dataBase.dislike_comment(comment_id)

    except Exception as e:

        return HTTPException(status_code=400, detail=str(e))

@app.post('/news/like')
async def like(post_id : str, auth : Optional[str] = Header(None, alias="Authorization")):

    try:

        return await dataBase.like(post_id)

    except Exception as e:

        return HTTPException(status_code=400, detail=str(e))
    
@app.post('/news/dislike')
async def dislike(post_id : str, auth : Optional[str] = Header(None, alias="Authorization")):

    try:

        return await dataBase.dislike(post_id)

    except Exception as e:

        return HTTPException(status_code=400, detail=str(e))
    
@app.get('/test')
def test(user_id : str):

    try:

        users = backend.get_users([user_id])

        return [
            {
                "id": user_id,
                "name": user.name,
                "email": user.email,
                "legend": user.legend,
                "avatar": user.avatar,
                "login": user.login,
                "reputationScore": user.reputationScore
            } for user in users
        ]

    except Exception as e:

        return HTTPException(status_code=400, detail=str(e))