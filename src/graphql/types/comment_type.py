# graphql/types/post.py
from __future__ import annotations
import strawberry
from typing import List, Optional
from ...models.comment_model import comment_model
from strawberry.scalars import JSON
from strawberry import Info

@strawberry.experimental.pydantic.type(model=comment_model)
class Comment:

    id : str = strawberry.field()
    post_id : strawberry.auto
    user_id: strawberry.auto
    text: strawberry.auto
    likes : strawberry.auto
    dislikes : strawberry.auto
    parent_id : Optional[str] = None
    replies : List[str] = strawberry.auto