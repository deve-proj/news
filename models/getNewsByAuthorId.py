from pydantic import BaseModel

class getNewsByAuthorId(BaseModel):

    author_id : str
    limit : int = 10