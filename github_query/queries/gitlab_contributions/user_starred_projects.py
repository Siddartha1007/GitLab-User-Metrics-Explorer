from github_query.model.query import QueryNode, PaginatedQuery, QueryNodePaginator

"""
{
  user(username: "dwt1") {
    username
    starredProjects {
      nodes {
        id
        name
        languages {
            name
            share
        }
    }
    }
  }
}
"""

class UserStarredProjects(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"username": "\"$user\""},
                    fields=[
                        "username",
                        QueryNodePaginator(
                            "starredProjects",
                            args={"first": "$pg_size"},
                            fields=[
                                QueryNode(
                                    "nodes",
                                    fields=[
                                        "id",
                                        "name",
                                        QueryNode(
                                            "languages",
                                            fields=["name", "share"],
                                        )]
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