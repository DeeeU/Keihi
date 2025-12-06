import strawberry
from typing import List


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello from Keihi GraphQL API"


schema = strawberry.Schema(query=Query)
