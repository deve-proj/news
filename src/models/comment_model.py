from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from fastapi import UploadFile, File

class comment_model(BaseModel):

    user_id : str
    text : str