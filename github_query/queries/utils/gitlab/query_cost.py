from github_query.model.query import Query, QueryNode


class GitLabQueryCost(Query):
    def __init__(self, test):
        super().__init__(
            fields=[
                test,
                QueryNode(
                    "queryComplexity",
                    fields=[
                        "limit",
                        "score"
                    ]
                )
            ]
        )
