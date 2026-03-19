from ..types.comment_type import Comment
from typing import List, Optional
from ...database.main import DataBase
from strawberry import Info

async def resolve_comments(info : Info, post_id : Optional[str] = None) -> List[Comment]:

    db = info.context['db']

    comments = []

    if post_id:

        comments = await db.get_comments(post_id)

    result = []

    for comment in comments:
        
        result.append(Comment(
            user_id=comment['user_id'],
            text=comment['text']
        ))

    return result