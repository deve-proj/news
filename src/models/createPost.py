from pydantic import BaseModel
from typing import Dict, Any

class create_post_model(BaseModel):

    title : str
    content : Dict[str, Any]