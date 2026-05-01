# graphql/types/post.py
import strawberry
from typing import List, Optional
from ...models.post_model import post_model, content_block
from strawberry.scalars import JSON
from .comment_type import Comment

@strawberry.experimental.pydantic.type(model=content_block)
class ContentBlock:
    type: strawberry.auto
    style: Optional[JSON] = None
    value: strawberry.auto

@strawberry.type
class UserData:
    id : str
    name : str
    login : str
    avatar_url : str

@strawberry.type
class Post:
    id: str
    user_data : UserData
    datetime: str
    views: str
    likes : str
    dislikes : str
    title: str
    preview_image: str
    category : str
    content: List[ContentBlock]
    comments: Optional[List[Comment]] = None