from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from fastapi import UploadFile, File

class comment_model(BaseModel):

    user_id : str
    post_id : str
    text : str
    likes : Optional[int] = 0
    dislikes : Optional[int] = 0
    replies : Optional[comment_model] = []
    parent_id : Optional[str] = None

    