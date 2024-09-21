import time
from abc import ABC

from github_query.model.client import Client
from github_query.queries.utils.gitlab.query_cost import GitLabQueryCost

class QueryComplexityError(Exception):
    pass

class GitLabClient(Client, ABC):

    def base_path(self):
        """
        Returns base path for a GraphQL Request.
        Returns:
            Base path for requests
        """
        return (
            f"{self._protocol}://{self._host}/graphql"
            if self._is_enterprise else
            f"{self._protocol}://{self._host}/api/graphql"
        )

    def handle_retry(self, match):
        rate_query = GitLabQueryCost(match.group('content'))
        query_complexity = self._retry_request(3, 10, rate_query, {"dryrun": True})
        query_complexity = query_complexity.json()["data"]["queryComplexity"]
        limit = query_complexity["limit"]
        score = query_complexity["score"]
        if score > limit:
            raise QueryComplexityError("Query is too complex. Please simplify query")

