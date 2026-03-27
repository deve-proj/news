from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from fastapi import UploadFile, File
from .comment_model import comment_model


class content_block(BaseModel):

    type : str
    style : Optional[dict] = None
    value : str
class post_data(BaseModel):

    title : str
    preview_image : str
    content : list[content_block]

class post_model(BaseModel):
    
    views: Optional[int] = 0
    likes: Optional[int] = 0
    dislikes: Optional[int] = 0
    user_id : str
    datetime : int
    post : post_data
    comments: Optional[List[comment_model]] = []