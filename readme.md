# GitHub Deployment Cleaner

A Python-based automation tool designed to streamline the management of GitHub deployments within a repository. The script simplifies the process of cleaning up outdated deployments, ensuring that your repository remains organized while retaining the most recent deployment.

---

## 🎯 **Purpose**
This script is designed for developers and DevOps engineers who manage GitHub repositories and need an automated way to clean up old deployments while keeping the repository organized.

---

## 📋 **Features**
- Lists all deployments in a GitHub repository.
- Marks old deployments as inactive.
- Deletes inactive deployments, keeping only the specified deployment ID.

---

## 🚀 **How It Works**
1. Fetches all deployments in the specified GitHub repository.
2. Retains the deployment specified by `KEEP_DEPLOYMENT_ID`.
3. Marks all other deployments as inactive.
4. Deletes the inactive deployments.

---

## 🛠️ **Prerequisites**
- Python 3.7 or higher.
- A valid **GitHub Personal Access Token** with appropriate permissions.
  - **Required Scopes**:
    - `repo` (if the repository is private).
    - `public_repo` (if the repository is public).

---

## 📦 **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/renbkna/github-deployment-cleaner.git
   cd github-deployment-cleaner
   ```

2. Install dependencies:
   ```bash
   pip install requests
   ```

3. Replace placeholders in the script with your details:
   - `TOKEN`: Your GitHub personal access token.
   - `USER`: Your GitHub username or organization name.
   - `REPO`: The name of your repository.
   - `KEEP_DEPLOYMENT_ID`: The ID of the deployment you want to keep.

---

## 🚀 **Usage**

Run the script:
```bash
python github-deployment-cleaner.py
```

- The script will:
  - Fetch all deployments.
  - Mark all but the specified deployment (`KEEP_DEPLOYMENT_ID`) as inactive.
  - Delete the inactive deployments.

---

## 🌟 **Example Output**
```bash
Keeping the latest deployment: ID <LATEST_DEPLOYMENT_ID>
Marked deployment ID <DEPLOYMENT_ID> as inactive.
Deleted deployment ID <DEPLOYMENT_ID>.
```

---

## ⚠️ **Important Notes**
- **Destructive Action**: This script deletes deployments permanently. Double-check `KEEP_DEPLOYMENT_ID` to avoid unintentional deletion.
- **GitHub API Rate Limits**: Ensure your token has sufficient API call limits for large repositories.

---

## 📜 **License**

This project is open-source and available under the [MIT License](LICENSE).

---
