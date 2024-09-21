from github_query.model.query import QueryNode, PaginatedQuery, QueryNodePaginator

"""
{
  user(username: "dwt1") {
    username
    projectMemberships {
        nodes {
          project {
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
}
"""

class UserContributedAndPersonalProjects(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"username": "\"$user\""},
                    fields=[
                        "username",
                        QueryNodePaginator(
                            "projectMemberships",
                            args={"first": "$pg_size"},
                            fields=[
                                QueryNode(
                                    "nodes",
                                    fields=[
                                        QueryNode(
                                            "project",
                                            fields=[
                                                "id",
                                                "name",
                                                QueryNode(
                                                    "languages",
                                                    fields=["name", "share"],
                                                )]
                                            )
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
            ]
        )