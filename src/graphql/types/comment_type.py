# graphql/types/post.py
import strawberry
from typing import List, Optional
from ...models.comment_model import comment_model
from strawberry.scalars import JSON

@strawberry.experimental.pydantic.type(model=comment_model)
class Comment:
    user_id: strawberry.auto
    text: strawberry.auto