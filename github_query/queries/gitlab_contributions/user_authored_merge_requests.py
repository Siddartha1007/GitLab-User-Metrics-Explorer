from github_query.model.query import QueryNode, PaginatedQuery, QueryNodePaginator


class UserAuthoredMergeRequests(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"username": "\"$user\""},
                    fields=[
                        "username",
                        QueryNodePaginator(
                            "authoredMergeRequests",
                            args={"first": "$pg_size"},
                            fields=[
                                "count",
                                QueryNode(
                                    "nodes",
                                    fields=["createdAt"]
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
