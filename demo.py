import os

from github_query.gitlab_graphql.gitlab_client import GitLabClient
from github_query.model.authentication import PersonalAccessTokenAuthenticator, GitLabPersonalAccessTokenAuthenticator
from github_query.github_graphql.github_client import GitHubClient
from github_query.queries.contributions.user_gists import UserGists
from github_query.queries.contributions.user_issues import UserIssues
from github_query.queries.contributions.user_pull_requests import UserPullRequests
from github_query.queries.contributions.user_repositories import UserRepositories
from github_query.queries.contributions.user_repository_discussions import UserRepositoryDiscussions
from github_query.queries.gitlab_contributions.user_assigned_merge_requests import UserAssignedMergeRequests
from github_query.queries.gitlab_contributions.user_authored_merge_requests import UserAuthoredMergeRequests
from github_query.queries.gitlab_contributions.user_authored_snippets import UserAuthoredSnippets 
from github_query.queries.gitlab_contributions.user_issues_contribution import UserIssuesContributions
from github_query.queries.gitlab_contributions.user_contributed_and_personal_projects import UserContributedAndPersonalProjects 
from github_query.queries.gitlab_contributions.user_starred_projects import UserStarredProjects
from github_query.queries.gitlab_contributions.user_authored_snippets import UserAuthoredSnippets 
from github_query.queries.gitlab_contributions.user_review_requested_merge_requests import \
    UserReviewRequestedMergeRequests

client = GitHubClient(
    host="api.github.com", is_enterprise=False,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
)

gitLab_client = GitLabClient(
    host="gitlab.com", is_enterprise=False,
    authenticator=GitLabPersonalAccessTokenAuthenticator(token=os.environ.get("GITLAB_ACCESS_TOKEN"))
)

account = "your_github_account_here"
for response in client.execute(query=UserGists(), substitutions={"user": account, "pg_size": 2}):
    print(response)

for response in client.execute(query=UserIssues(), substitutions={"user": account, "pg_size": 2}):
    print(response)

for response in client.execute(query=UserPullRequests(), substitutions={"user": account, "pg_size": 2}):
    print(response)

for response in client.execute(query=UserRepositoryDiscussions(),substitutions={"user": account, "pg_size": 2}):
    print(response)

for response in client.execute(query=UserRepositories(), substitutions={"user": account, "pg_size": 5,"is_fork": True,"ownership": "OWNER",
                                                                        "order_by": {"field": "CREATED_AT","direction": "ASC"}}):
    print(response)

gitLab_account = "your_gitlab_account_here"
for response in gitLab_client.execute(query=UserAssignedMergeRequests(), substitutions={"user": gitLab_account, "pg_size": 2}):
    print(response)

for response in gitLab_client.execute(query=UserAuthoredMergeRequests(), substitutions={"user": gitLab_account, "pg_size": 2}):
    print(response)

for response in gitLab_client.execute(query=UserReviewRequestedMergeRequests(), substitutions={"user": gitLab_account, "pg_size": 2}):
    print(response)

for response in gitLab_client.execute(query=UserAuthoredSnippets(), substitutions={"user": gitLab_account, "pg_size": 2}):
    print(response)

for response in gitLab_client.execute(query=UserIssuesContributions(), substitutions={"user": gitLab_account, "pg_size": 2}):
    print(response)

for response in gitLab_client.execute(query=UserContributedAndPersonalProjects(), substitutions={"user": gitLab_account, "pg_size": 2}):
    print(response)

for response in gitLab_client.execute(query=UserStarredProjects(), substitutions={"user": gitLab_account, "pg_size": 2}):
    print(response)
