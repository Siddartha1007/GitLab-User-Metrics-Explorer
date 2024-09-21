from abc import ABC

from github_query.model.client import Client

class MockClient(Client, ABC):
    def base_path(self):
        """
        Returns base path for a Mock Request.
        Returns:
            Base path for requests
        """
        return (
            f"{self._protocol}://{self._host}/enterprise"
            if self._is_enterprise else
            f"{self._protocol}://{self._host}/not/enterprise"
        )

    def handle_retry(self, match):
        return
