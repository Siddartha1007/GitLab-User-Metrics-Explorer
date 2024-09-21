import pytest
import requests.exceptions

from github_query.model.authentication import PersonalAccessTokenAuthenticator
from github_query.model.client import InvalidAuthenticationError, QueryFailedException
from github_query.queries.gitlab_contributions.user_assigned_merge_requests import UserAssignedMergeRequests
from github_query.queries.gitlab_contributions.user_authored_snippets import UserAuthoredSnippets 
from github_query.queries.gitlab_contributions.user_starred_projects import UserStarredProjects
from github_query.queries.gitlab_contributions.user_contributed_and_personal_projects import UserContributedAndPersonalProjects
from github_query.tests.helpers.mock_client import MockClient
from github_query.queries.gitlab_contributions.user_issues_contribution import UserIssuesContributions



class TestClient:

    mock_paginated_response_user_issues_contributions = {
        "data": {
            "issues": {
                "nodes": [
                    {
                        "createdAt": "2022-01-01T16:10:04Z", 
                        "title": "Issue 1"
                    }
                ],
                "pageInfo": {
                    "endCursor": None, 
                    "hasNextPage": False
                }
            }
        }
    }

    
    mock_paginated_response_with_next_page = {
        "data": {
            "user": {
                "username": "tester",
                "assignedMergeRequests": {
                    "count": 1,
                    "nodes": [
                        {
                            "createdAt": "2022-04-17T21:12:06Z"
                        }
                    ],
                    "pageInfo": {
                        "endCursor": "eyJjcmVhdGVkX2F0IjoiMjAyMS0xMS0yNyAyMjo0MzozNy45NzYxNTUwMDAgKzAwMDAiLCJpZCI6IjEyODE0MDY4MCJ9",
                        "hasNextPage": True
                    }
                }
            },
            "queryComplexity": {
                "limit": 250,
                "score": 13
            }
        }
    }

    mock_paginated_response_without_next_page = {
        "data": {
            "user": {
                "username": "tester",
                "assignedMergeRequests": {
                    "count": 1,
                    "nodes": [
                        {
                            "createdAt": "2022-04-17T21:12:06Z"
                        }
                    ],
                    "pageInfo": {
                        "endCursor": "eyJjcmVhdGVkX2F0IjoiMjAyMS0xMS0yNyAyMjo0MzozNy45NzYxNTUwMDAgKzAwMDAiLCJpZCI6IjEyODE0MDY4MCJ9",
                        "hasNextPage": False
                    }
                }
            },
            "queryComplexity": {
                "limit": 250,
                "score": 13
            }
        }
    }

    mock_paginated_response_without_next_page_for_snippets = {
        "data": {
            "user": {
                "username": "tester",
                "snippets": {
                    "nodes": [ 
                        {
                            "createdAt": "2022-04-17T21:12:06Z",
                            "description": "Mock Project",
                            "id": "007",
                            "title": "Mock Project",
                            "webUrl": "gitlab.io/jamesbond/mockproject",
                            "visibilityLevel": "public"
                        }
                    ],
                    "pageInfo": {
                        "endCursor": "eyJjcmVhdGVkX2F0IjoiMjAyMS0xMS0yNyAyMjo0MzozNy45NzYxNTUwMDAgKzAwMDAiLCJpZCI6IjEyODE0MDY4MCJ9",
                        "hasNextPage": False
                    }
                },
            },
            "queryComplexity": {
                "limit": 250,
                "score": 13
            }
        }
    }

    mock_paginated_response_without_next_page_for_starred_projects = {
        "data": {
            "user": {
                "username": "tester",
                "starredProjects": {
                    "nodes": [ 
                        {
                            "id": "0007",
                            "name": "Mock Project"
                        }
                    ],
                    "pageInfo": {
                        "endCursor": "eyJjcmVhdGVkX2F0IjoiMjAyMS0xMS0yNyAyMjo0MzozNy45NzYxNTUwMDAgKzAwMDAiLCJpZCI6IjEyODE0MDY4MCJ9",
                        "hasNextPage": False
                    }
                },
            },
            "queryComplexity": {
                "limit": 250,
                "score": 13
            }
        }
    }

    mock_paginated_response_without_next_page_for_contributed_and_personal_projects = {
        "data": {
            "user": {
                "username": "tester",
                "projectMemberships": {
                    "nodes": [ 
                        {
                            "project" : [
                                {
                                    "id": "0007",
                                    "name": "Mock Project"
                                }
                            ],
                        },
                    ],
                    "pageInfo": {
                        "endCursor": "eyJjcmVhdGVkX2F0IjoiMjAyMS0xMS0yNyAyMjo0MzozNy45NzYxNTUwMDAgKzAwMDAiLCJpZCI6IjEyODE0MDY4MCJ9",
                        "hasNextPage": False
                    }
                },
            },
            "queryComplexity": {
                "limit": 250,
                "score": 13
            }
        }
    }

    @pytest.fixture
    def client(self):
        return MockClient(host="some_url", authenticator=PersonalAccessTokenAuthenticator(token="token"))


    def test_authenticator_none(self):
        with pytest.raises(InvalidAuthenticationError):
            MockClient(host="some_host")
    def test_execute_with_string_query_no_substitutions_empty_results(self, client, requests_mock):
        mocked_result = []
        requests_mock.post("https://some_url/not/enterprise", json={"data": mocked_result})

        result = client.execute(query="query", substitutions={})

        assert len(result) == 0
        assert result == mocked_result

    def test_execute_with_string_query_no_substitutions_one_result(self, client, requests_mock):
        mocked_result = [{"someKey": "someValue"}]
        requests_mock.post("https://some_url/not/enterprise", json={"data": mocked_result })

        result = client.execute(query="query", substitutions={})

        assert len(result) == 1
        assert result == mocked_result

    def test_execute_with_string_query_no_substitutions_requests_timeout(self, client, requests_mock):
        requests_mock.post("https://some_url/not/enterprise", exc=requests.exceptions.Timeout)

        with pytest.raises(QueryFailedException):
            client.execute(query="query", substitutions={})

    def test_execute_with_string_query_no_substitutions_requests_status_404(self, client, requests_mock):
        requests_mock.post("https://some_url/not/enterprise", json={"error": "error"}, status_code=404)

        with pytest.raises(QueryFailedException):
            client.execute(query="query", substitutions={})

    def test_execute_with_paginated_query_no_substitutions_one_result(self, client, requests_mock):
        requests_mock.post("https://some_url/not/enterprise", [{'json': self.mock_paginated_response_with_next_page},
                                                               {'json': self.mock_paginated_response_without_next_page}])

        for response in client.execute(query=UserAssignedMergeRequests(), substitutions={"user": "tester", "pg_size": 2}):
            assert response["user"]["username"] == "tester

    def test_execute_with_paginated_query_user_issues_contributions(self, client, requests_mock):
        requests_mock.post(
            "https://some_url/not/enterprise",
            [{'json': self.mock_paginated_response_user_issues_contributions},
            {'json': self.mock_paginated_response_user_issues_contributions}]
        )
        for response in client.execute(query=UserIssuesContributions(), substitutions={"user": "tester", "pg_size": 10}):
            assert len(response["issues"]["nodes"]) == 1
            assert response["issues"]["nodes"][0]["title"] == "Issue 1"
            
    def test_execute_with_paginated_query_no_substitutions_one_result_snippets(self, client, requests_mock):
        requests_mock.post("https://some_url/not/enterprise", [{'json': self.mock_paginated_response_without_next_page_for_snippets}])
                                                      
        for response in client.execute(query=UserAuthoredSnippets(), substitutions={"user": "tester", "pg_size": 2}):
            assert response["user"]["username"] == "tester"

    def test_execute_with_paginated_query_no_substitutions_one_result_starredProjects(self, client, requests_mock):
        requests_mock.post("https://some_url/not/enterprise", [{'json': self.mock_paginated_response_without_next_page_for_starred_projects}])
                                                      
        for response in client.execute(query=UserStarredProjects(), substitutions={"user": "tester", "pg_size": 2}):
            assert response["user"]["username"] == "tester"

    def test_execute_with_paginated_query_no_substitutions_one_result_ContributedandPersonalProjects(self, client, requests_mock):
        requests_mock.post("https://some_url/not/enterprise", [{'json': self.mock_paginated_response_without_next_page_for_contributed_and_personal_projects}])
                                                      
        for response in client.execute(query=UserContributedAndPersonalProjects(), substitutions={"user": "tester", "pg_size": 2}):
            assert response["user"]["username"] == "tester"
