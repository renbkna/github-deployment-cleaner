import os
import requests
import logging
import asyncio
import httpx
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv

# Load the .env file from one hierarchy above the current file's directory (root of the project)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Use environment variable for token; GitHub user and repo will be entered dynamically
TOKEN = os.environ.get("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Asynchronous function to fetch the latest status for a deployment
async def fetch_status_async(statuses_url: str) -> str:
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


def list_deployments(base_url: str = None):
    """
    List all deployments along with their latest status fetched asynchronously.
    If base_url is not provided, it falls back to a default value.
    """
    if base_url is None:
        messagebox.showerror("Error", "Repository URL is not defined.")
        return []
    response = requests.get(base_url, headers=HEADERS)
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


def mark_inactive(deployment_id, base_url: str = None):
    """
    Mark a deployment as inactive.
    """
    if base_url is None:
        messagebox.showerror("Error", "Repository URL is not defined.")
        return False
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


def delete_deployment(deployment_id, base_url: str = None):
    """
    Delete a deployment.
    """
    if base_url is None:
        messagebox.showerror("Error", "Repository URL is not defined.")
        return False
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


# ----------------------------
# GUI using Tkinter
# ----------------------------
class GitHubDeploymentGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GitHub Deployment Cleaner")
        self.geometry("900x600")
        # Dictionary to store full deployment data keyed by Treeview row ID.
        self.tree_data = {}
        self.create_widgets()
        self.bind_tree_events()

    def create_widgets(self):
        # Frame for repository configuration
        frame_repo = ttk.Frame(self)
        frame_repo.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(frame_repo, text="GitHub Username:").pack(side=tk.LEFT, padx=5)
        self.entry_username = ttk.Entry(frame_repo, width=20)
        self.entry_username.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_repo, text="Repository Name:").pack(side=tk.LEFT, padx=5)
        self.entry_repo = ttk.Entry(frame_repo, width=20)
        self.entry_repo.pack(side=tk.LEFT, padx=5)

        self.btn_list = ttk.Button(
            frame_repo, text="List Deployments", command=self.list_deployments
        )
        self.btn_list.pack(side=tk.LEFT, padx=10)

        # Treeview for showing deployments with extra columns for actions
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Ref", "Status", "Created At", "Mark", "Delete"),
            show="headings",
            height=20,
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Ref", text="Ref")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Created At", text="Created At")
        self.tree.heading("Mark", text="Mark Inactive")
        self.tree.heading("Delete", text="Delete")
        self.tree.column("ID", width=100)
        self.tree.column("Ref", width=150)
        self.tree.column("Status", width=100)
        self.tree.column("Created At", width=180)
        self.tree.column("Mark", width=120)
        self.tree.column("Delete", width=120)
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Status label
        self.status_label = ttk.Label(self, text="Ready")
        self.status_label.pack(pady=5)

    def bind_tree_events(self):
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

    def update_status(self, message):
        self.status_label.config(text=message)

    def get_base_url(self):
        username = self.entry_username.get().strip()
        repo = self.entry_repo.get().strip()
        if not username or not repo:
            messagebox.showerror(
                "Error", "Please enter both GitHub username and repository name."
            )
            return None
        return f"https://api.github.com/repos/{username}/{repo}/deployments"

    def list_deployments(self):
        base_url = self.get_base_url()
        if not base_url:
            return

        def task():
            self.update_status("Fetching deployments...")
            deployments = list_deployments(base_url=base_url)
            self.tree.delete(*self.tree.get_children())
            self.tree_data.clear()
            for dep in deployments:
                dep_id = dep.get("id")
                dep_ref = dep.get("ref")
                dep_status = dep.get("state", "unknown")
                created_at = dep.get("created_at", "N/A")
                mark_text = "[Mark Inactive]"
                delete_text = (
                    "[Delete]" if dep_status == "inactive" else "[Delete Disabled]"
                )
                row_id = self.tree.insert(
                    "",
                    "end",
                    values=(
                        dep_id,
                        dep_ref,
                        dep_status,
                        created_at,
                        mark_text,
                        delete_text,
                    ),
                )
                self.tree_data[row_id] = dep
            self.update_status("Fetched deployments.")

        threading.Thread(target=task).start()

    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not row_id:
            return

        dep = self.tree_data.get(row_id)
        if not dep:
            return

        deployment_id = dep.get("id")
        current_status = dep.get("state")
        base_url = self.get_base_url()
        if not base_url:
            return

        # If the user clicks on the "Mark Inactive" column
        if col == "#5":
            if current_status == "inactive":
                messagebox.showinfo("Info", "Deployment is already inactive.")
                return
            self.threaded_mark_inactive(deployment_id, base_url)
        elif col == "#6":  # Delete column
            if current_status != "inactive":
                messagebox.showerror(
                    "Error", "You can only delete an inactive deployment."
                )
                return
            self.threaded_delete_deployment(deployment_id, base_url)

    def threaded_mark_inactive(self, deployment_id, base_url):
        def task():
            self.update_status(f"Marking deployment {deployment_id} as inactive...")
            success = mark_inactive(deployment_id, base_url=base_url)
            if success:
                messagebox.showinfo(
                    "Success", f"Deployment {deployment_id} marked as inactive."
                )
            else:
                messagebox.showerror(
                    "Error", f"Failed to mark deployment {deployment_id} as inactive."
                )
            self.update_status("Operation complete.")
            self.list_deployments()

        threading.Thread(target=task).start()

    def threaded_delete_deployment(self, deployment_id, base_url):
        if not messagebox.askyesno(
            "Confirm", f"Are you sure you want to delete deployment {deployment_id}?"
        ):
            return

        def task():
            self.update_status(f"Deleting deployment {deployment_id}...")
            success = delete_deployment(deployment_id, base_url=base_url)
            if success:
                messagebox.showinfo(
                    "Success", f"Deployment {deployment_id} deleted successfully."
                )
            else:
                messagebox.showerror(
                    "Error", f"Failed to delete deployment {deployment_id}."
                )
            self.update_status("Operation complete.")
            self.list_deployments()

        threading.Thread(target=task).start()


if __name__ == "__main__":
    app = GitHubDeploymentGUI()
    app.mainloop()
