# GitHub Deployment Cleaner

GitHub Deployment Cleaner is a tool that helps you manage and clean up deployments in your GitHub repositories. It features a Python CLI built with Click that interacts with the GitHub API to list, mark, and delete deployments.

## Table of Contents

- [Features](#features)
- [Repository Structure](#repository-structure)
- [Setup Guide (Local Development)](#setup-guide-local-development)
  - [Backend CLI Setup](#backend-cli-setup)
  - [Using the CLI](#using-the-cli)
- [API Endpoints (For Reference)](#api-endpoints-for-reference)
- [Deployment Guide](#deployment-guide)
- [Using VS Code](#using-vs-code)
- [Running Both Backend and Frontend](#running-both-backend-and-frontend)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- **List Deployments:** Retrieve all deployments for a specified GitHub repository.
- **Mark as Inactive:** Update a deployment’s status to "inactive".
- **Delete Deployment:** Remove a deployment.
- **Asynchronous Optimization:** Asynchronous HTTP calls using `httpx` and `asyncio` for faster concurrent status fetching.
- **Command-Line Interface:** A CLI tool built with Click (`cli.py`) for direct terminal usage.

## Repository Structure

```plaintext
├── frontend/                   # React frontend (if needed)
│   ├── ...
│   └── package.json            # Contains scripts for running the frontend
│
├── github-deployment-cleaner/  # Python backend & CLI tool
│   ├── cli.py                # Command-line tool for managing deployments
│   ├── github_deployments.py # GitHub API interaction functions (if needed)
│   ├── app.py                # (Optional) Flask API server version
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment configuration file (not included in repo)
│
└── README.md                   # This file
```

## Setup Guide (Local Development)

### Backend CLI Setup

1. **Clone the Repository & Install Dependencies:**

   ```bash
   git clone https://github.com/renbkna/github-deployment-cleaner.git
   cd github-deployment-cleaner
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   pip install -r github-deployment-cleaner/requirements.txt
   ```

2. **Configure Environment Variables:**

   Create a `.env` file inside the `github-deployment-cleaner/` directory with the following content:

   ```ini
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_USER=your_github_username
   GITHUB_REPO=your_github_repo_name
   FLASK_SECRET_KEY=your_secret_key
   ```

### Using the CLI

The CLI tool is contained in `github-deployment-cleaner/cli.py` and uses Click to provide the following commands:

- **List Deployments:**

  ```bash
  python github-deployment-cleaner/cli.py list
  ```

  This command will print the ID, reference, status, and creation date of each deployment.

- **Mark a Deployment as Inactive:**

  ```bash
  python github-deployment-cleaner/cli.py mark <deployment_id>
  ```

  Replace `<deployment_id>` with the actual ID of the deployment you wish to mark as inactive.

- **Delete a Deployment:**

  ```bash
  python github-deployment-cleaner/cli.py delete <deployment_id>
  ```

  Replace `<deployment_id>` with the actual ID of the deployment you wish to delete.

## API Endpoints (For Reference)

_Note: The CLI is intended for direct command-line use. However, if you run the Flask server version (`app.py`), the following endpoints are available:_

| Method | Endpoint                                         | Description                   |
| ------ | ------------------------------------------------ | ----------------------------- |
| GET    | `/api/deployments`                               | Fetch all deployments         |
| POST   | `/api/deployments/<deployment_id>/mark_inactive` | Mark a deployment as inactive |
| DELETE | `/api/deployments/<deployment_id>`               | Delete a deployment           |

## Deployment Guide

### Deploying the Backend on a Server

1. **Deploy the CLI as a Scheduled Job or Service:**
   You can wrap the CLI commands in shell scripts or scheduled tasks (e.g., using cron on Linux/Windows Task Scheduler) to run them periodically.

2. **Or, Use the Flask Version:**
   If you prefer a web API, the Flask-based `app.py` is also available. Deploy it using a production WSGI server (e.g., Gunicorn) following your hosting provider’s instructions.

## Using VS Code

You can run and test the CLI tool directly within Visual Studio Code:

1. **Integrated Terminal:**
   Open the VS Code terminal and run commands like:

   ```bash
   python github-deployment-cleaner/cli.py list
   python github-deployment-cleaner/cli.py mark 123456
   python github-deployment-cleaner/cli.py delete 123456
   ```

2. **Debug Configuration:**
   You can create a `launch.json` configuration to run the CLI with specific arguments. For example:

   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Run CLI List Command",
         "type": "python",
         "request": "launch",
         "program": "${workspaceFolder}/github-deployment-cleaner/cli.py",
         "args": ["list"],
         "console": "integratedTerminal"
       }
     ]
   }
   ```

   This allows you to run and debug the CLI directly from VS Code.

## Running Both Backend and Frontend

If you want to run both the Python backend (using `app.py`) and the Next.js frontend concurrently with a single command, you can use the `concurrently` package. Make sure your repository structure looks like this:

```plaintext
root/
├── .venv/                    # Virtual environment (in the repository root)
├── github-deployment-cleaner/
│   └── app.py                # Flask API server version
└── frontend/
    └── package.json          # Contains scripts for running the frontend
```

Then, in your `frontend/package.json`, update or add the following script:

```json
"dev:all": "concurrently \"..\\\\.venv\\\\Scripts\\\\python.exe ..\\\\github-deployment-cleaner\\\\app.py\" \"next dev\""
```

> **Note for Windows Users:**
> Backslashes are escaped (`\\`) in JSON. This command assumes that your virtual environment is in the repository root.
> On macOS/Linux, you would use:
> `"dev:all": "concurrently \"../.venv/bin/python ../github-deployment-cleaner/app.py\" \"next dev\""`

To run both backend and frontend concurrently, open your terminal in the `frontend` folder and execute:

```bash
npm run dev:all
```

This command will:

- Start your Flask backend by executing the Python file from your virtual environment.
- Start the Next.js frontend development server.

## Troubleshooting

- **No Deployments Listed:**
  Ensure your environment variables in `.env` are set correctly and that your GitHub token has the proper permissions.

- **Slow Responses:**
  The CLI uses asynchronous HTTP calls to fetch statuses concurrently. If delays persist, check your network connectivity or GitHub API rate limits.

- **CLI Errors:**
  Make sure you are running the script in the correct virtual environment and that all dependencies are installed.

- **Path Issues on Windows:**
  Verify that the paths in the `dev:all` script are correct relative to your `frontend` folder. Adjust the backslashes if needed.

## License

This project is licensed under the [MIT License](LICENSE).
