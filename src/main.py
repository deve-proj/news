from fastapi import FastAPI
#from models.getNewsByAuthorId import getNewsByAuthorId
from .database.main import dataBase

app = FastAPI()
database = dataBase()

@app.get('/news')
async def getNews():

    return {

        "status": 200,


    }

@app.get('/news/')
async def getNewsByAuthorId(authorId : int):

    result = await database.getPostsByAuthorId(authorId)

    return {

        "status": 200,
        "posts": result

    }