import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from github_deployments import list_deployments, mark_inactive, delete_deployment
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

console = Console()


@click.group()
def cli():
    """GitHub Deployments CLI"""
    pass


@cli.command()
def list():
    """List all deployments."""
    deployments = list_deployments()
    if not deployments:
        console.print("[bold red]No deployments found.[/bold red]")
        return

    table = Table(title="GitHub Deployments")
    table.add_column("ID", style="cyan")
    table.add_column("Ref", style="magenta")
    table.add_column("State", style="green")
    table.add_column("Created At", style="yellow")

    for d in deployments:
        table.add_row(
            str(d.get("id")),
            d.get("ref", "N/A"),
            d.get("state", "unknown"),
            d.get("created_at", "N/A"),
        )

    console.print(table)


@cli.command()
@click.argument("deployment_id", type=int)
def mark(deployment_id):
    """Mark a deployment as inactive."""
    if mark_inactive(deployment_id):
        console.print(
            f"[bold green]Deployment {deployment_id} marked as inactive.[/bold green]"
        )
    else:
        console.print(
            f"[bold red]Failed to mark deployment {deployment_id} as inactive.[/bold red]"
        )


@cli.command()
@click.argument("deployment_id", type=int)
def delete(deployment_id):
    """Delete a deployment."""
    if Confirm.ask(f"Are you sure you want to delete deployment {deployment_id}?"):
        if delete_deployment(deployment_id):
            console.print(
                f"[bold green]Deployment {deployment_id} deleted successfully.[/bold green]"
            )
        else:
            console.print(
                f"[bold red]Failed to delete deployment {deployment_id}.[/bold red]"
            )
    else:
        console.print("Operation cancelled.")


@cli.command()
def clean():
    """Clean deployments (keep only the latest)."""
    deployments = list_deployments()
    if not deployments:
        console.print("[bold red]No deployments found.[/bold red]")
        return

    # Assume the first deployment in the list is the most recent.
    latest_deployment = deployments[0]
    console.print(
        f"[bold blue]Keeping the latest deployment: ID {latest_deployment.get('id')}[/bold blue]"
    )

    for d in deployments[1:]:
        deployment_id = d.get("id")
        if mark_inactive(deployment_id) and delete_deployment(deployment_id):
            console.print(f"[green]Cleaned deployment {deployment_id}.[/green]")
        else:
            console.print(f"[red]Failed to clean deployment {deployment_id}.[/red]")


if __name__ == "__main__":
    cli()
