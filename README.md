# Python Version
We provide a convenient tool to query a user's GitHub metrics.

**IN ORDER TO USE THIS TOOL, YOU NEED TO PROVIDE YOUR OWN .env FILE.**
Because we use the [dotenv](https://pypi.org/project/python-dotenv/) package to load environment variable.
**YOU ALSO NEED TO PROVIDE YOUR GITHUB PERSONAL ACCESS TOKEN(PAT) IN YOUR .env FILE**
i.e. GITHUB_TOKEN  = 'your_access_token'

## Installation

We recommend using virtual environment. 
```shell
cd path/to/your/project/directory
python -m venv venv
```
On macOS and Linux:
```shell
source venv/bin/activate
```
On Windows (Command Prompt):
```shell
.\venv\Scripts\activate
```
On Windows (PowerShell):
```shell
.\venv\Scripts\Activate.ps1
```
then you can
```shell
pip install -r requirements.txt
```

## Execution
TBD

### authentication  — Basic authenticator class
Source code: [github_query/model/authentication.py]()

This module provides the basic authentication mechanism. User needs to provide a valid GitHub PAT with correct scope to run queries. 
A PersonalAccessTokenAuthenticator object will be created with the PAT that user provided. get_authorization_header method will return an
 authentication header that will be used when send request to GitHub GraphQL server.

<span style="font-size: larger;">Authenticator Objects</span>

Parent class of PersonalAccessTokenAuthenticator. Serve as base class of any authenticators.

<span style="font-size: larger;">PersonalAccessTokenAuthenticator Objects</span>

Handles personal access token authentication method for GitHub clients.

`class PersonalAccessTokenAuthenticator(token)`
* The `token` argument is required. This is the user's GitHub personal access token with the necessary scope to execute the queries that the user required.

Instance methods:

`get_authorization_header()`
* Returns the authentication header as a dictionary i.e. {"Authorization": "your_access_token"}.

### query  — Classes for building GraphQL queries
Source code: [github_query/model/query.py]()

This module provides a framework for building GraphQL queries using Python classes. The code defines four classes: QueryNode, QueryNodePaginator, Query, and PaginatedQuery.
QueryNode represents a basic building block of a GraphQL query. 
QueryNodePaginator is a specialized QueryNode for paginated requests. 
Query represents a terminal query node that can be executed. 
PaginatedQuery represents a terminal query node designed for paginated requests.
* You can find more information about GitHub GraphQL API here: [GitHub GraphQL API documentation](https://docs.github.com/en/graphql)
* You can use GitHub GraphQL Explorer to try out queries: [GitHub GraphQL API Explorer](https://docs.github.com/en/graphql/overview/explorer)

<span style="font-size: larger;">QueryNode Objects</span>

The QueryNode class provides a framework for constructing GraphQL queries using Python classes. 
It allows for building complex queries with nested fields and supports pagination for paginated requests.

`class QueryNode(name, fields, args)`
* `name` is the name of the QueryNode
* `fields` is a List of fields in the QueryNode
* `args` is a Map of arguments in the QueryNode.

Private methods:

`_format_args()`
* _format_args method takes the arguments of a QueryNode instance and formats them as a string representation in the form of key-value pairs. The formatting depends on the type of the argument value, with special handling for strings, lists, dictionaries, booleans, and the default case for other types. The method then returns the formatted arguments as a string enclosed within parentheses.

`_format_fields()`
* _format_fields method takes the list of fields within a QueryNode instance and formats them as a single string representation.

Instance methods:

`get_connected_nodes()`
* get_connected_nodes method returns a list of connected QueryNode instances within a QueryNode instance. It iterates over the fields attribute of the QueryNode instance and checks if each field is an instance of QueryNode. The resulting list contains all the connected QueryNode instances found.

`__str__()`
* \__str\__ method defines how the QueryNode object should be represented as a string. It combines the object's name, formatted arguments, and formatted fields to construct the string representation in a specific format.

`__repr__()`
* Debug method.

`__eq__(other)`
* \__eq\__ method defines how the QueryNode object should be compared to each other. 
 

<span style="font-size: larger;">Query Objects</span>

The Query class is a subclass of QueryNode and represents a terminal QueryNode that can be executed. 
It provides a substitute method to substitute values in the query using keyword arguments.

Class methods:

`test_time_format(time_string)`
* test_time_format is a static method that validates whether a given time string is in the expected format "%Y-%m-%dT%H:%M:%SZ".

`convert_dict(data)`
* convert_dict is a static method that takes a dictionary (data) as input and returns a modified dictionary with certain value conversions.
* If the value is of type bool, it converts it to a lowercase string representation.
* If the value is a nested dictionary, it converts it to a string representation enclosed in curly braces.
* If the value is a string and passes the test_time_format check, it wraps it in double quotes.
* For other value types, it keeps the value unchanged.

Instance methods:

`substitute(**kwargs)`
* This method substitutes the placeholders in the query string with specific values provided as keyword arguments.

<span style="font-size: larger;">QueryNodePaginator Objects</span>

The QueryNodePaginator class extends the QueryNode class and adds pagination-related functionality. 
It keeps track of pagination state, appends pagination fields to the existing fields, 
provides methods to check for a next page and update the pagination state, 
and includes a method to reset the pagination state.

#### NOTE: We only implemented single level pagination, as multi-level pagination behavior is not well-defined in different scenarios. For example, you want to query all the pull requests a user made to all his/her repositories. You may develop a query that retrieves all repositories of a user as the first level pagination and all pull requests to each repository as the second level pagination. However, each repository not necessarily has the same number of pull requests. We leave this to the user to decide how they want to handle their multi-level pagination.

`class QueryNodePaginator(name, fields, args)`
* `name` is the name of the QueryNode.
* `fields` is a List of fields in the QueryNode. 
* `args` is a Map of arguments in the QueryNode.

Instance methods:

`update_paginator(has_next_page, end_cursor)`
* update_paginator updates the paginator arguments with the provided has_next_page and end_cursor values. It adds the end cursor to the arguments using the key "after", enclosed in double quotes.

`has_next()`
* The has_next method checks if there is a next page by returning the value of has_next_page.

`reset_paginator()`
* The reset_paginator method resets the QueryPaginator by removing the "after" key from the arguments and setting has_next_page to None.

`__eq__(other)`
* \__eq\__ method overrides the equality comparison for QueryNodePaginator objects. It compares the object against another object of the same class, returning True if they are equal based on the parent class's equality comparison (super().__eq__(other)).


<span style="font-size: larger;">PaginatedQuery Objects</span>

`class PaginatedQuery(name, fields, args)`
* `name` is the name of the QueryNode
* `fields` is a List of fields in the QueryNode
* `args` is a Map of arguments in the QueryNode.
* The \__init\__ method initializes a PaginatedQuery object with the provided name, fields, and arguments. It calls the parent class's __init__ method and then extracts the path to the pageInfo node using the extract_path_to_pageinfo_node static method.

`extract_path_to_pageinfo_node(paginated_query)`
* The extract_path_to_pageinfo_node static method is used to extract the path to the QueryNodePaginator node within the query. It takes a PaginatedQuery object as input and traverses the query fields to find the QueryNodePaginator. It returns a tuple containing the path to the QueryNodePaginator node and the QueryNodePaginator node. If the QueryNodePaginator node is not found, it raises an InvalidQueryException.

### client  — 
Source code: [github_query/model/client.py]()

This abstract class represents the main GraphQL client.

`class Client(protocol, host, is_enterprise, authenticator)`
* `protocol`: Protocol used for server communication.
* `host`: Host server domain or IP.
* `is_enterprise`: Boolean to check if the host is running on Enterprise.
* `authenticator`: The authentication handler for the client.

Private methods:

`_generate_headers(self, **kwargs)`:
* Generates headers for an HTTP request, including authentication headers and other additional headers passed as keyword arguments.

`_retry_request(self, retry_attempts, timeout_seconds, query, substitutions)`:
* Wrapper method to retry requests. Takes in the number of attempts, timeout duration, the query, and the substitutions for the query.

`_execute(self, query, substitutions)`:
* Executes a GraphQL query after performing the required substitutions. Handles possible request errors and rate limiting.

`_execution_generator(self, query, substitutions)`:
* Executes a PaginatedQuery by repeatedly querying until all pages have been fetched. Yields each response.

Instance methods:

`execute(self, query, substitutions):`
* Executes a query, which can be a simple Query or a PaginatedQuery. Utilizes the _execute method or the _execution_generator method based on the type of query.

Abstract methods:

`base_path(self)`:
* This is an abstract method and should be overridden by each client (GitHub or GitLab).
* Returns the base path for a GraphQL request based on whether the client is connected to Enterprise.

`handle_retry(self)`:
* This is an abstract method and should be overridden by each client (GitHub or GitLab).
* Handles the retry conditions for the GitHub Client.

### github_client
Source code: [github_query/github_graphql/github_client.py]()

This is the client that represents GitHub.

`class GitHubClient(protocol, host, is_enterprise, authenticator)`
* Extends Client. Please refer above

Overriden methods:

`base_path(self)`:
* Returns the GraphQL paths based on whether the client is connected to GitHub Enterprise

`handle_retry(self)`:
* Handles retrying requests with GitHub's rate limit.

### gitlab_client
Source code: [github_query/gitlab_graphql/gitlab_client.py]()

This is the client that represents GitLab.

`class GitLabClient(protocol, host, is_enterprise, authenticator)`
* Extends Client. Please refer above

Overriden methods:

`base_path(self)`:
* Returns the GraphQL paths based on whether the client is connected to GitLab Enterprise

`handle_retry(self)`:
* Handles retrying requests with GitLab's query complexity limits.

### contributions  —  Query for retrieving contributions made by a user
Source code: [queries/contributions.py]()

UserIssues represents a GraphQL query for retrieving issue contributions made by a user. The query structure includes a "user" field with the user's login as an argument. Inside the "user" field, there is a nested field "QueryNodePaginator". 
This field represents the pagination of contributions made by the user. The value of "$pg_size" sets the number of contributions to retrieve per page.
Inside the "QueryNodePaginator" field, there are several requested fields. These fields include "totalCount" to get the total count of contributions, "nodes" to retrieve the contribution nodes with their creation timestamps, and "pageInfo" to fetch pagination information such as the end cursor and whether there are more pages available.

#### NOTE: contribution_type can be any valid contribution type such as "issues" or "pullRequests"
<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query($user: String!, $pg_size: Int!){
    user(login: $user){
        login
        issues(first:$pg_size){
            totalCount
            pageInfo{
                hasNextPage
                endCursor
            }
            nodes{
                createdAt
            }
        }
    }
}
```

</td>
<td>

```python
def __init__(self):
    super().__init__(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    "login",
                    QueryNodePaginator(
                        "issues",
                        args={"first": "$pg_size"},
                        fields=[
                            "totalCount",
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
```
</td>
</tr>
</table>


### Snippets — Query for retrieving snippetes created by a user

UserAuthoredSnippets represents a GraphQL query for retrieving snippets (a.k.a gists on GitHub) created by a user on GitLab. The query structure includes a "user" field with the user's login as an argument. Inside the "user" field, there is a nested field "QueryNodePaginator", which includes pagination of repositories. there is a nested field "nodes", which includes information of the snippet node. "CreatedAt" indicates the information when snippet was created, "Description" indicates description of the snippet, "id" indicates the unique ID with which GitLab stores the snippet with, "title" indicates the title with which the snippet is stored, "webUrl" indicates the URL to access the snippet with and "visibilityLevel" indicates who can access the snippet.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
{
  user(username: "username") {
    username
    snippets(first: 10) {
      nodes {
        createdAt
        description
        id
        title
        webUrl
        visibilityLevel
      }
    }
  }
}

```

</td>
<td>

```python
class UserAuthoredSnippets(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"username": "\"$user\""},
                    fields=[
                        "username",
                        QueryNodePaginator(
                            "snippets",
                            args={"first": "$pg_size"},
                            fields=[
                                QueryNode(
                                    "nodes",
                                    fields=["createdAt", "description", "id", "title", "webUrl", "visibilityLevel"]
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
```
</td>
</tr>
</table>


### repositories  — Query for retrieving repositories owned or contributed to by a user
Source code: [queries/user_repositories.py]()

UserRepositories represents a GraphQL query for retrieving repositories owned or contributed to by a user. The query structure includes a "user" field with the user's login as an argument. Inside the "user" field, there is a nested field "QueryNodePaginator". 
This field represents the pagination of repositories. The "QueryNodePaginator" field accepts several arguments that allow for filtering and ordering the repositories. These arguments include "$pg_size" to set the pagination size, "$is_fork" to filter by whether the repository is a fork, "$ownership" to filter by owner affiliations, and "$order_by" to specify the field and direction for ordering the repositories.
Inside the "QueryNodePaginator" field, there are several requested fields. These fields include "nodes" to retrieve information about the repositories. Each repository node includes various details such as the repository name, whether it is empty, creation and update timestamps, fork count, stargazer count, total watcher count, primary programming language, and information about the languages used in the repository.
The "languages" field provides information about the languages used in the repository. It accepts additional arguments for filtering and ordering the languages. The requested fields within the "languages" field include "totalSize" to get the total size of the languages used, "totalCount" to get the count of distinct languages, and "edges" to retrieve detailed information about each language, including its size and name.

#### NOTE: isFork can be "True" or "False", ownerAffiliation can be "OWNER" or "COLLABORATOR"
<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query($user: String!, $pg_size: Int!, $isFork: Boolean!, $ownerAffiliations: [RepositoryAffiliation!]!) {
    user(login: $user) {
        repositories(first: $pg_size, isFork: $isFork, ownerAffiliations: $ownerAffiliations, orderBy: { field: CREATED_AT, direction: ASC }) {
            totalCount
            pageInfo {
                hasNextPage
                endCursor
            }
            nodes {
                name
                isEmpty
                createdAt
                updatedAt
                forkCount
                stargazerCount
                watchers {
                    totalCount
                }
                primaryLanguage {
                    name
                }
                languages(first: 100) {
                    totalSize
                    totalCount
                    edges {
                        size
                        node {
                            name
                        }
                    }
                }
            }
        }
    }
}
```

</td>
<td>

```python
def __init__(self):
    super().__init__(
        fields=[
            QueryNode(
                "user",
                args={"login": "$user"},
                fields=[
                    QueryNodePaginator(
                        "repositories",
                        args={"first": "$pg_size",
                              "isFork": "$is_fork",
                              "ownerAffiliations": "$ownership",
                              "orderBy": "$order_by"},
                        fields=[
                            QueryNode(
                                "nodes",
                                fields=[
                                    "name",
                                    "isEmpty",
                                    "createdAt",
                                    "updatedAt",
                                    "forkCount",
                                    "stargazerCount",
                                    QueryNode("watchers", fields=["totalCount"]),
                                    QueryNode("primaryLanguage", fields=["name"]),
                                    QueryNode(
                                        "languages",
                                        args={"first": 100,
                                              "orderBy": {"field": "SIZE",
                                                          "direction": "DESC"}},
                                        fields=[
                                            "totalSize",
                                            "totalCount",
                                            QueryNode(
                                                "edges",
                                                fields=[
                                                    "size",
                                                    QueryNode("node", fields=["name"])
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),
                            QueryNode(
                                "pageInfo",
                                fields=["endCursor", "hasNextPage"]
                            )
                        ]
                    ),
                ]
            )
        ]
    )
```
</td>
</tr>
</table>


GitLab divides the repositories into two types:

1. Starred repositores - These are the repositores the user has starred for reference.

    In the below schema, username corresponds to the username in the GitLab instance and the id, name correspond to the project id and the project name.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
{
  user(username: "dwt1") {
    username
    starredProjects {
      nodes {
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
```

</td>
<td>

```python
class UserStarredProjects(PaginatedQuery):
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"username": "\"$user\""},
                    fields=[
                        "username",
                        QueryNodePaginator(
                            "starredProjects",
                            args={"first": "$pg_size"},
                            fields=[
                                QueryNode(
                                    "nodes",
                                    fields=[
                                        "id",
                                        "name",
                                        QueryNode(
                                            "languages",
                                            fields=["name", "share"],
                                        )]
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
```
</td>
</tr>
</table>

2. Contributed and Personal repositories - These are the repositores the user has contributed to which are maintained by others and the personal repositores which the user owns and maintains.


    In the below schema, username corresponds to the username in the GitLab instance and the id, name correspond to the project id and the project name.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
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
```
</td>
<td>

```python
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

```
</td>
</tr>
</table>


### Pull Requests — Query for retrieving pull requests that a user contributed to in GitHub.
Source code: [queries/contributions/user_pull_requests.py]()

UserPullRequests represents a GraphQL query for retrieving pull requests associated to a user in GitHub. The query structure includes a "user" field with the user's login as an argument. Inside the "user" field, there is a nested field "QueryNodePaginator". 
This field represents the pagination of repositories. The "QueryNodePaginator" field accepts a few arguments that allow for filtering and ordering the repositories. These arguments include "$pg_size" to set the pagination size.
Inside the "QueryNodePaginator" field, there are several requested fields. These fields include "nodes" to retrieve information about the repositories. Each pull request node includes the date and time that the pull request was created.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query($user: String!, $pg_size: Int!: [PullRequestConnection!]!) {
    user(login: $user) {
        pullRequests(first: $pg_size) {
            totalCount
            nodes {
                createdAt
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
}
```

</td>
<td>

```python
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"login": "$user"},
                    fields=[
                        "login",
                        QueryNodePaginator(
                            "pullRequests",
                            args={"first": "$pg_size"},
                            fields=[
                                "totalCount",
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
```
</td>
</tr>
</table>

### Merge Requests — Queries for retrieving merge requests that a user was assigned to, authored, or a review was requested in GitLab. 
Source code: [queries/contributions/user_pull_requests.py]()

_UserAssignedMergeRequests_ represents a GraphQL query for retrieving merge requests that a user was assigned to in GitLab. The query structure includes a "user" field with the user's username as an argument. Inside the "user" field, there is a nested field "QueryNodePaginator". 
This field represents the pagination of repositories. The "QueryNodePaginator" field accepts a few arguments that allow for filtering and ordering the repositories. These arguments include "$pg_size" to set the pagination size.
Inside the "QueryNodePaginator" field, there are several requested fields. These fields include "nodes" to retrieve information about the repositories. Each merge request node includes the date and time that the pull request was created.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query($user: String!, $pg_size: Int!: [MergeRequestConnection!]!) {
    user(username: "$user") {
        assignedMergeRequests(first: $pg_size) {
            count
            nodes {
                createdAt
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
}
```

</td>
<td>

```python
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
```
</td>
</tr>
</table>

_UserAuthoredMergeRequests_ represents a GraphQL query for retrieving merge requests that a user authored in GitLab. The query structure includes a "user" field with the user's username as an argument. Inside the "user" field, there is a nested field "QueryNodePaginator". 
This field represents the pagination of repositories. The "QueryNodePaginator" field accepts a few arguments that allow for filtering and ordering the repositories. These arguments include "$pg_size" to set the pagination size.
Inside the "QueryNodePaginator" field, there are several requested fields. These fields include "nodes" to retrieve information about the repositories. Each merge request node includes the date and time that the pull request was created.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query($user: String!, $pg_size: Int!: [MergeRequestConnection!]!) {
    user(username: "$user") {
        authoredMergeRequests(first: $pg_size) {
            count
            nodes {
                createdAt
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
}
```

</td>
<td>

```python
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"username": "\"$user\""},
                    fields=[
                        "username",
                        QueryNodePaginator(
                            "authoredMergeRequests",
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
```
</td>
</tr>
</table>

_UserReviewRequestedMergeRequests_ represents a GraphQL query for retrieving merge requests assigned to the user for review in GitLab. The query structure includes a "user" field with the user's username as an argument. Inside the "user" field, there is a nested field "QueryNodePaginator". 
This field represents the pagination of repositories. The "QueryNodePaginator" field accepts a few arguments that allow for filtering and ordering the repositories. These arguments include "$pg_size" to set the pagination size.
Inside the "QueryNodePaginator" field, there are several requested fields. These fields include "nodes" to retrieve information about the repositories. Each merge request node includes the date and time that the pull request was created.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query($user: String!, $pg_size: Int!: [MergeRequestConnection!]!) {
    user(username: "$user") {
        reviewRequestedMergeRequests(first: $pg_size) {
            count
            nodes {
                createdAt
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
}
```

</td>
<td>

```python
    def __init__(self):
        super().__init__(
            fields=[
                QueryNode(
                    "user",
                    args={"username": "\"$user\""},
                    fields=[
                        "username",
                        QueryNodePaginator(
                            "reviewRequestedMergeRequests",
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
```
</td>
</tr>
</table>

### ratelimit  — 
Source code: [queries/rate_limit.py](https://github.com/JialinC/GitHub_GraphQL/blob/main/python_github_query/queries/rate_limit.py)

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
query ($dryrun: Boolean!){
  rateLimit (dryRun: $dryrun){
    cost
    limit
    remaining
    resetAt
    used
  }
}

```

</td>
<td>

```python
```
</td>
</tr>
</table>



### GitLab contributions  —  Query for retrieving user issues contributions
Source code: [queries/gitlab_contributions](https://github.ncsu.edu/jcui9/G2371/tree/main/github_query/queries/gitlab_contributions)

UserIssuesContributions class represents a GraphQL query specifically designed to fetch paginated issue contributions by a specific user on GitLab. This query is structured to obtain detailed information about each issue posted by the user. The core component of this query is the QueryNodePaginator, which handles the pagination of the issues. It is configured with two arguments: $pg_size determines the number of issue items to retrieve in a single page of results, and authorUsername is a filter that specifies the username of the author whose issues are being queried. Inside the "QueryNodePaginator" field, there are several requested fields. These fields include "Count" to get the total count of contributions, "nodes" to retrieve the contribution nodes with their creation timestamps, title, id, description, updated timestamp,the url to access the issue on the web, current state of the issue(open/closed) and "pageInfo" to fetch pagination information such as the end cursor and whether there are more pages available.

<table>
<tr>
<th>GraphQL</th>
<th>Python</th>
</tr>
<tr>
<td>

```
{
  issues(first: 10, authorUsername: "$user") {
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
```

</td>
<td>

```python
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

```
</td>
</tr>
</table>

### Limitations of current GitLab infrastucture - 

1. Currently, GitLab doesn't provide the schema to get information on Rate Limiting.

    GitHub supports this and a crawler can use this information to adjust while querying. Information is only provided on the complexity of a query and the max possible complexity of the query.

2. Currently, GitLab doesn't have a feature called User repository discussion unlike GitHub.

    Since, there is no such feature on GitLab, there is no schema to support this.

3. If a user has contributed to a repository inside another repository i.e a subrepository. That information is not displayed when queried for contributed projects of a user on GitLab. This is another limitation of GitLab schema.

These three were the limitations of the current GitLab infrastructure, which resulted in differences in mapping with all current
GitHub features.

