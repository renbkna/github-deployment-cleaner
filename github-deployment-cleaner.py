import requests

TOKEN = "YOUR_GITHUB_TOKEN"  # Replace with your GitHub token
USER = "YOUR_USER_NAME"  # Replace with your GitHub username or organization name
REPO = "YOUR_REPO_NAME"  # Replace with the name of the repository
KEEP_DEPLOYMENT_ID = "YOUR_KEEP_DEPLOYMENT_ID"  # Replace with the ID of the deployment to keep

BASE_URL = f"https://api.github.com/repos/{USER}/{REPO}/deployments"
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}


def list_deployments():
    """List all deployments in the repository."""
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch deployments: {response.status_code}")
        print(response.json())
        return []


def mark_inactive(deployment_id):
    """Mark a deployment as inactive."""
    url = f"{BASE_URL}/{deployment_id}/statuses"
    payload = {"state": "inactive"}
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 201:
        print(f"Marked deployment ID {deployment_id} as inactive.")
    else:
        print(
            f"Failed to mark deployment ID {deployment_id} as inactive: {response.status_code}"
        )
        print(response.json())


def delete_deployment(deployment_id):
    """Delete a deployment."""
    url = f"{BASE_URL}/{deployment_id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"Deleted deployment ID {deployment_id}.")
    else:
        print(f"Failed to delete deployment ID {deployment_id}: {response.status_code}")
        print(response.json())


def main():
    deployments = list_deployments()
    if not deployments:
        print("No deployments found.")
        return

    # Keep only the most recent deployment
    latest_deployment_id = deployments[0]["id"]
    print(f"Keeping the latest deployment: ID {latest_deployment_id}")

    for deployment in deployments[1:]:
        deployment_id = deployment["id"]
        mark_inactive(deployment_id)  # Mark as inactive before deletion
        delete_deployment(deployment_id)  # Delete the deployment


if __name__ == "__main__":
    main()
