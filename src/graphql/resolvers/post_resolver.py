from ..types.post_type import Post, ContentBlock, UserData
from typing import List, Optional
from ...database.database import DataBase
from strawberry import Info
from ..types.comment_type import Comment

async def resolve_posts(info : Info, user_id : Optional[str] = None, amount : Optional[int] = 1) -> List[Post]:

    db = info.context['db']
    comment_loader = info.context['comment_loader']

    reply_loader = info.context['reply_loader']
    user_loader = info.context['user_loader']

    posts = []
    
    if user_id:

        try:

            posts = await db.get_posts_by_user_id(user_id)

        except Exception as e:

            raise e

    else:

        try:

            posts = await db.get_all_posts()

        except Exception as e:

            raise e

    result = []

    if len(posts) != 0:

        for i in range(amount):
        
            post = posts[i]

            post_id_str = str(post['_id'])

            comment_data = await comment_loader.load(post_id_str)

            userData = await user_loader.load(post['user_id'])

            comments = [
                Comment(
                    id=str(c['_id']),
                    user_id=c['user_id'],
                    post_id=c['post_id'],
                    text=c['text'],
                    likes=c.get('likes', 0),
                    dislikes=c.get('dislikes', 0),
                    replies=[]
                )
                for c in comment_data
            ]

            content_block = [
                ContentBlock(
                    type=block["type"],
                    style=block["style"],
                    value=block["value"]
                )

                for block in post['content']
            ]

            result.append(Post(
                id=str(post['_id']),
                user_data=UserData(
                    id=userData.id,
                    name=userData.name,
                    avatar_url=userData.avatar,
                    login=userData.login
                ),
                datetime=post['datetime'],
                title=post['title'],
                preview_image=post['preview_image'],
                content=content_block,
                views=post['views'],
                likes=post['likes'],
                dislikes=post['dislikes'],
                category=post['category'],
                comments=comments
            ))

    return result

async def resolve_post_by_id(info : Info, post_id : str) -> Optional[Post]:

    db = info.context['db']
    comment_loader = info.context['comment_loader']
    reply_loader = info.context['reply_loader']
    backend = info.context["backend_client"]

    post = await db.get_post_by_post_id(post_id)

    post_id_str = str(post['_id'])

    comment_data = await comment_loader.load(post_id_str)

    userData = backend.get_user(post['user_id'])

    comments = [
        Comment(
            id=str(c['_id']),
            user_id=c['user_id'],
            post_id=c['post_id'],
            text=c['text'],
            likes=c.get('likes', 0),
            dislikes=c.get('dislikes', 0),
            replies=[]
        )
        for c in comment_data
    ]

    content_block = [
        ContentBlock(
            type=block["type"],
            style=block["style"],
            value=block["value"]
        )

        for block in post['content']
    ]

    return Post(
        id=str(post['_id']),
        user_data=UserData(
            id=post["user_id"],
            name=userData.name,
            avatar_url=userData.avatar,
            login=userData.login
        ),
        datetime=post['datetime'],
        title=post['title'],
        preview_image=post['preview_image'],
        content=content_block,
        views=post['views'],
        likes=post['likes'],
        dislikes=post['dislikes'],
        category=post['category'],
        comments=comments
    )