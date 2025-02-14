import os
import requests
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Load configuration from environment variables
TOKEN = os.environ.get("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN")
USER = os.environ.get("GITHUB_USER", "YOUR_USER_NAME")
REPO = os.environ.get("GITHUB_REPO", "YOUR_REPO_NAME")
BASE_URL = f"https://api.github.com/repos/{USER}/{REPO}/deployments"
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_deployments():
    """List all deployments in the repository along with their state."""
    response = requests.get(BASE_URL, headers=HEADERS)
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


def mark_inactive(deployment_id):
    """Mark a deployment as inactive."""
    url = f"{BASE_URL}/{deployment_id}/statuses"
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


def delete_deployment(deployment_id):
    """Delete a deployment."""
    url = f"{BASE_URL}/{deployment_id}"
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
    deployments = list_deployments()
    return jsonify(deployments)


@app.route("/api/deployments/<int:deployment_id>/mark_inactive", methods=["POST"])
def api_mark_inactive(deployment_id):
    success = mark_inactive(deployment_id)
    return jsonify({"success": success})


@app.route("/api/deployments/<int:deployment_id>", methods=["DELETE"])
def api_delete_deployment(deployment_id):
    success = delete_deployment(deployment_id)
    return jsonify({"success": success})


if __name__ == "__main__":
    app.run(debug=True)
