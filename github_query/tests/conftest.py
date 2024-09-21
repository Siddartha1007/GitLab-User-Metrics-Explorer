import os
import pytest
from github_query.model.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.github_client import GitHubClient


@pytest.fixture(scope="module")
def graphql_client():
    # Set up the GraphQL client
    client = GitHubClient(
        host="api.github.com", is_enterprise=False,
        authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
    )

    enterprise_client = GitHubClient(
        host="github.ncsu.edu", is_enterprise=True,
        authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_ENTERPRISE_PERSONAL_ACCESS_TOKEN"))
    )
    yield [client, enterprise_client]


@pytest.fixture(autouse=True)
def inject_graphql_clients(request, graphql_client):
    client, enterprise_client = graphql_client

    request.cls.client = client

    request.cls.enterprise_client = enterprise_client
