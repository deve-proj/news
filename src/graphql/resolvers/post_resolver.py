from ..types.post_type import Post, PostData, ContentBlock
from typing import List, Optional
from ...database.main import DataBase
from strawberry import Info

async def resolve_posts(info : Info, user_id : Optional[str] = None, post_id : Optional[str] = None) -> List[Post]:

    db = info.context['db']

    posts = []

    if post_id:

        posts = [await db.get_post_by_post_id(post_id)]
    
    elif user_id:

        posts = await db.get_posts_by_user_id(user_id)

    else:

        posts = await db.get_all_posts()

    result = []

    for post in posts:

        content_block = [
            ContentBlock(
                type=block["type"],
                style=block["style"],
                value=block["value"]
            )

            for block in post['post']['content']
        ]

        post_data = PostData(
            title=post['post']['title'],
            preview_image=post['post']['preview_image'],
            content=content_block
        )

        result.append(Post(
            id=str(post['_id']),
            user_id=post['user_id'],
            datetime=post['datetime'],
            post=post_data
        ))

    return result