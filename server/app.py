import os
import requests
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

# Load the .env file from one directory above the current file's directory (root of the project)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Get GitHub token from .env (always from .env)
TOKEN = os.environ.get("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN")

# The following USER and REPO are fallback defaults if none are provided dynamically.
DEFAULT_USER = os.environ.get("GITHUB_USER", "YOUR_USER_NAME")
DEFAULT_REPO = os.environ.get("GITHUB_REPO", "YOUR_REPO_NAME")
DEFAULT_BASE_URL = (
    f"https://api.github.com/repos/{DEFAULT_USER}/{DEFAULT_REPO}/deployments"
)

HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_base_url(username: str = None, repo: str = None):
    """
    Construct the GitHub API URL for deployments.
    If username and repo are provided, use them; otherwise, use default values.
    """
    if username and repo:
        return f"https://api.github.com/repos/{username}/{repo}/deployments"
    return DEFAULT_BASE_URL


def list_deployments(base_url: str):
    """List all deployments in the repository along with their state."""
    response = requests.get(base_url, headers=HEADERS)
    if response.status_code != 200:
        logger.error(
            f"Failed to fetch deployments: {response.status_code} {response.json()}"
        )
        return []

    deployments = response.json()

    # For each deployment, fetch its latest status
    for deployment in deployments:
        statuses_url = deployment.get("statuses_url")
        if statuses_url:
            status_resp = requests.get(statuses_url, headers=HEADERS)
            if status_resp.status_code == 200:
                statuses = status_resp.json()
                # Assuming the first status is the latest
                if statuses:
                    deployment["state"] = statuses[0].get("state")
                else:
                    deployment["state"] = "pending"
            else:
                deployment["state"] = "unknown"
        else:
            deployment["state"] = "unknown"

    return deployments


def mark_inactive(deployment_id, base_url: str):
    """Mark a deployment as inactive."""
    url = f"{base_url}/{deployment_id}/statuses"
    payload = {"state": "inactive"}
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        logger.info(f"Deployment {deployment_id} marked as inactive.")
        return True
    else:
        logger.error(
            f"Failed to mark deployment {deployment_id} as inactive: {response.status_code} {response.json()}"
        )
        return False


def delete_deployment(deployment_id, base_url: str):
    """Delete a deployment."""
    url = f"{base_url}/{deployment_id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        logger.info(f"Deployment {deployment_id} deleted successfully.")
        return True
    else:
        logger.error(
            f"Failed to delete deployment {deployment_id}: {response.status_code} {response.json()}"
        )
        return False


app = Flask(__name__, static_folder="./frontend/build", static_url_path="/")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your_secret_key")
CORS(app)  # Enable CORS for all routes


@app.route("/")
def serve():
    """
    In production (when the React app is built) this will serve the index.html.
    In development (npm run dev) you typically load the React dev server.
    """
    return app.send_static_file("index.html")


@app.route("/api/deployments", methods=["GET"])
def api_list_deployments():
    # Get username and repo dynamically from query parameters
    username = request.args.get("username")
    repo = request.args.get("repo")
    base_url = get_base_url(username, repo)
    deployments = list_deployments(base_url)
    return jsonify(deployments)


@app.route("/api/deployments/<int:deployment_id>/mark_inactive", methods=["POST"])
def api_mark_inactive(deployment_id):
    username = request.args.get("username")
    repo = request.args.get("repo")
    base_url = get_base_url(username, repo)
    success = mark_inactive(deployment_id, base_url)
    return jsonify({"success": success})


@app.route("/api/deployments/<int:deployment_id>", methods=["DELETE"])
def api_delete_deployment(deployment_id):
    username = request.args.get("username")
    repo = request.args.get("repo")
    base_url = get_base_url(username, repo)
    success = delete_deployment(deployment_id, base_url)
    return jsonify({"success": success})


if __name__ == "__main__":
    app.run(debug=True)
