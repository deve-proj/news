import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from ..database.database import DataBase
from .types.post_type import Post
from .types.comment_type import Comment
from .resolvers.post_resolver import resolve_posts, resolve_post_by_id
from .dataloaders.comment_loader import CommentLoader
from .dataloaders.reply_loader import ReplyLoader
from ..clients.backend.backendClient import BackendClient
from .dataloaders.user_loader import UserLoader

async def get_graphql_context():

    return {
        "db": DataBase(),
        "comment_loader": CommentLoader(DataBase()),
        "reply_loader": ReplyLoader(DataBase()),
        "user_loader": UserLoader(BackendClient())
    }

@strawberry.type
class Query:

    posts: List[Post] = strawberry.field(
        resolver=resolve_posts,
        description="Получить все посты"
    )

    post : Post = strawberry.field(
        resolver=resolve_post_by_id,
        description="Получить пост по id"
    )

graphql_schema = strawberry.Schema(query=Query)

graphql_router = GraphQLRouter(
    graphql_schema,
    context_getter=get_graphql_context,
    path="/graphql"
)