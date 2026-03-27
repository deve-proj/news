# graphql/types/post.py
import strawberry
from typing import List, Optional
from ...models.post_model import post_model, post_data, content_block
from strawberry.scalars import JSON
from .comment_type import Comment

@strawberry.experimental.pydantic.type(model=content_block)
class ContentBlock:
    type: strawberry.auto
    style: Optional[JSON] = None
    value: strawberry.auto

@strawberry.experimental.pydantic.type(model=post_data)
class PostData:
    title: strawberry.auto
    preview_image: strawberry.auto
    content: List[ContentBlock]

@strawberry.experimental.pydantic.type(model=post_model)
class Post:
    id: str = strawberry.field()
    user_id: strawberry.auto
    datetime: strawberry.auto
    views: strawberry.auto
    likes : strawberry.auto
    dislikes : strawberry.auto
    post: PostData
    comments: Optional[List[Comment]] = None