from github_query.model.query import QueryNode, PaginatedQuery, QueryNodePaginator


class UserAssignedMergeRequests(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"username": "\"$user\""},
                    fields=[
                        "username",
                        QueryNodePaginator(
                            "assignedMergeRequests",
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
