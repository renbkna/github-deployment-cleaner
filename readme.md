# GitHub Deployment Cleaner

A Python script to manage and clean up deployments in a GitHub repository. It automates marking old deployments as inactive and deleting them, keeping the most recent deployment active.

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

## 📝 **Environment Variables (Optional)**

Instead of hardcoding sensitive information like `TOKEN`, you can use environment variables for better security.

1. Export the environment variables:
   ```bash
   export GITHUB_TOKEN="your_token_here"
   export GITHUB_USER="your_username_here"
   export GITHUB_REPO="your_repo_here"
   export GITHUB_KEEP_DEPLOYMENT_ID="your_deployment_id_here"
   ```

2. Modify the script to read from environment variables:
   ```python
   import os

   TOKEN = os.getenv("GITHUB_TOKEN")
   USER = os.getenv("GITHUB_USER")
   REPO = os.getenv("GITHUB_REPO")
   KEEP_DEPLOYMENT_ID = os.getenv("GITHUB_KEEP_DEPLOYMENT_ID")
   ```

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

## 👨‍💻 **Contributing**

Contributions are welcome! Feel free to:
1. Fork the repository.
2. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature name"
   ```
4. Push the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## 📜 **License**

This project is open-source and available under the [MIT License](LICENSE).

---