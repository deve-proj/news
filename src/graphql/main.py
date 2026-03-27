import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from ..database.main import DataBase
from .types.post_type import Post
from .types.comment_type import Comment
from .resolvers.post_resolver import resolve_posts
from .dataloaders.comment_loader import CommentLoader
from .dataloaders.reply_loader import ReplyLoader

async def get_graphql_context():

    return {
        "db": DataBase(),
        "comment_loader": CommentLoader(DataBase()),
        "reply_loader": ReplyLoader(DataBase())
    }

@strawberry.type
class Query:

    news: List[Post] = strawberry.field(
        resolver=resolve_posts,
        description="Получить все посты"
    )

graphql_schema = strawberry.Schema(query=Query)

graphql_router = GraphQLRouter(
    graphql_schema,
    context_getter=get_graphql_context,
    path="/graphql"
)