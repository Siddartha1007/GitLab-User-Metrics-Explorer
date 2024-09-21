from github_query.model.query import QueryNode, PaginatedQuery, QueryNodePaginator

"""
{
  user(username: "abhi_kirk") {
        username
    snippets(first: 10) {
      nodes {
        createdAt
        description
        id
        title
        webUrl
        visibilityLevel
      }
    }
  }
}
"""

class UserAuthoredSnippets(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"username": "\"$user\""},
                    fields=[
                        "username",
                        QueryNodePaginator(
                            "snippets",
                            args={"first": "$pg_size"},
                            fields=[
                                QueryNode(
                                    "nodes",
                                    fields=["createdAt", "description", "id", "title", "webUrl", "visibilityLevel"]
                                ),
                                QueryNode(
                                    "pageInfo",
                                    fields=["endCursor", "hasNextPage"]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
