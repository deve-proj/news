from ...database.main import DataBase
from typing import Callable, Optional
from functools import wraps
from fastapi import Header, HTTPException
from ...common.jwtDecryptor import JWTDecryptor

def require_post_owner():

    db = DataBase()

    def decorator(endpoint_func : Callable):

        @wraps(endpoint_func)
        async def wrapper(*args, **kwargs):

            try:
                
                post_id = kwargs.get("post_id")
                jwt = JWTDecryptor(kwargs.get("auth"))

                post_data = (await db.get_post_by_post_id(post_id))

                if jwt.extract_user_id() != post_data["user_id"]:

                    raise HTTPException(status_code=401)
                
                return await endpoint_func(*args, **kwargs)

            except Exception as error:

                raise HTTPException(status_code=401, detail=str(error))
        
        return wrapper
    
    return decorator