from flask import Flask
from flask_cors import CORS
import os

from github_query.model.authentication import PersonalAccessTokenAuthenticator
from github_query.github_graphql.github_client import GitHubClient
from github_query.queries.contributions.user_login import UserLogin

app = Flask(__name__)

# Allow all origins to access routes with '/api/' prefix
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize GitHub client
client = GitHubClient(
    host="api.github.com", is_enterprise=False,
    authenticator=PersonalAccessTokenAuthenticator(token=os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN"))
)

@app.route('/api/github/userlogin')
def fetch_github_data():
    response = client.execute(
            query=UserLogin(), substitutions={"user": "torvalds"}
        )
    return response

# Run the app on 0.0.0.0
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)