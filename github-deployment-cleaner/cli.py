import os
import requests
import logging
import asyncio
import httpx
import click
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


async def fetch_status_async(statuses_url: str) -> str:
    """Fetch the latest status for a deployment asynchronously."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(statuses_url, headers=HEADERS)
            if response.status_code == 200:
                statuses = response.json()
                if statuses:
                    return statuses[0].get("state", "pending")
                else:
                    return "pending"
            else:
                logger.error(
                    f"Error fetching status from {statuses_url}: {response.status_code} {response.json()}"
                )
                return "unknown"
    except Exception as e:
        logger.error(f"Exception fetching status from {statuses_url}: {e}")
        return "unknown"


def run_async_tasks(tasks):
    """Run asynchronous tasks using a new event loop."""
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(asyncio.gather(*tasks))
        return results
    finally:
        loop.close()


def list_deployments():
    """List all deployments along with their latest status fetched asynchronously."""
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        logger.error(
            f"Failed to fetch deployments: {response.status_code} {response.json()}"
        )
        return []
    deployments = response.json()

    tasks = []
    deployments_with_tasks = []
    for deployment in deployments:
        statuses_url = deployment.get("statuses_url")
        if statuses_url:
            tasks.append(fetch_status_async(statuses_url))
            deployments_with_tasks.append(deployment)
        else:
            deployment["state"] = "unknown"

    if tasks:
        states = run_async_tasks(tasks)
        # Assign fetched state to each corresponding deployment
        for deployment, state in zip(deployments_with_tasks, states):
            deployment["state"] = state

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


@click.group()
def cli():
    """GitHub Deployment Cleaner CLI."""
    pass


@cli.command("list")
def cli_list():
    """List all deployments with their statuses."""
    deployments = list_deployments()
    if not deployments:
        click.echo("No deployments found.")
        return

    for dep in deployments:
        click.echo(f"ID: {dep.get('id')}")
        click.echo(f"Ref: {dep.get('ref')}")
        click.echo(f"Status: {dep.get('state', 'unknown')}")
        click.echo(f"Created at: {dep.get('created_at')}")
        click.echo("-" * 40)


@cli.command("mark")
@click.argument("deployment_id", type=int)
def cli_mark(deployment_id):
    """Mark a deployment as inactive by its DEPLOYMENT_ID."""
    if mark_inactive(deployment_id):
        click.echo(f"Deployment {deployment_id} marked as inactive.")
    else:
        click.echo(f"Failed to mark deployment {deployment_id} as inactive.")


@cli.command("delete")
@click.argument("deployment_id", type=int)
def cli_delete(deployment_id):
    """Delete a deployment by its DEPLOYMENT_ID."""
    if delete_deployment(deployment_id):
        click.echo(f"Deployment {deployment_id} deleted successfully.")
    else:
        click.echo(f"Failed to delete deployment {deployment_id}.")


if __name__ == "__main__":
    cli()
