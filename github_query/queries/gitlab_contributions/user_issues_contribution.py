from github_query.model.query import QueryNode, PaginatedQuery, QueryNodePaginator

"""
{
  issues(first: 10, authorUsername: "abhi_kirk") {
    nodes {
      createdAt
      title
      id
      description
      updatedAt
      webUrl
      state
    }
  }
}

"""

class UserIssuesContributions(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNodePaginator(
                    "issues",
                    args={"first": "$pg_size", "authorUsername": "\"$user\""},
                    fields=[
                        QueryNode(
                            "nodes",
                            fields=[
                                "createdAt",
                                "title",
                                "id",
                                "description",
                                "updatedAt",
                                "webUrl",
                                "state"
                            ]
                        ),
                        QueryNode(
                            "pageInfo",
                            fields=["endCursor", "hasNextPage"]
                        )
                    ]
                )
            ]
        )
