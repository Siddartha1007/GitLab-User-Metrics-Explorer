from abc import ABC
from datetime import datetime
import time

from github_query.model.client import Client
from github_query.queries.utils.query_cost import QueryCost


class GitHubClient(Client, ABC):

    def base_path(self):
        """
        Returns base path for a GraphQL Request.
        Returns:
            Base path for requests
        """
        return (
            f"{self._protocol}://{self._host}/api/graphql"
            if self._is_enterprise else
            f"{self._protocol}://{self._host}/graphql"
        )

    def handle_retry(self, match):
        rate_query = QueryCost(match.group('content'))
        rate_limit = self._retry_request(3, 10, rate_query, {"dryrun": True})
        rate_limit = rate_limit.json()["data"]["rateLimit"]
        cost = rate_limit['cost']
        remaining = rate_limit['remaining']
        reset_at = rate_limit['resetAt']
        if cost > remaining - 5:
            current_time = datetime.utcnow()
            time_format = '%Y-%m-%dT%H:%M:%SZ'
            reset_at = datetime.strptime(reset_at, time_format)
            time_diff = reset_at - current_time
            seconds = time_diff.total_seconds()
            print(f"stop at {current_time}s.")
            print(f"waiting for {seconds}s.")
            print(f"reset at {reset_at}s.")
            time.sleep(seconds + 5)
