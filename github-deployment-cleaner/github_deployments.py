import os
import requests
import logging
from dotenv import load_dotenv

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
    """List all deployments in the repository."""
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(
            f"Failed to fetch deployments: {response.status_code} {response.json()}"
        )
        return []


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
