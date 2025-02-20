# GitHub Deployment Cleaner

A lightweight tool to manage GitHub deployments by listing, marking inactive, and deleting them through a simple GUI and a REST API backend.

---

## Overview

- **Frontend:** A Next.js web interface that shows deployment details and actions.
- **Backend:** A Flask API that communicates with GitHub using your personal access token.
- **GUI (Standalone):** A Tkinter-based desktop app for deployment management.

---

## Features

- **List Deployments:** Retrieve deployments for a specified GitHub repository.
- **Mark Inactive:** Mark an active deployment as inactive. (Prevents redundant API calls if already inactive.)
- **Delete Deployment:** Delete a deployment (only enabled when the deployment is inactive).
- **Dynamic Configuration:** Enter GitHub username and repository name at runtime.
- **Secure Authentication:** Uses a GitHub personal access token stored in a `.env` file.

---

## Prerequisites

- **Node.js** (v16+)
- **npm**
- **Python 3.7+**
- **pip**
- A GitHub Personal Access Token with the **repo** scope (for full control)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/renbkna/github-deployment-cleaner
cd github-deployment-cleaner
```

### 2. Setup the Backend

- Navigate to the `server/` directory:
  
  ```bash
  cd server
  ```

- Create and activate a virtual environment:
  
  - **Windows:**

    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

  - **macOS/Linux:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

- Install dependencies:
  
  ```bash
  pip install -r requirements.txt
  ```

### 3. Setup the Frontend

- Navigate to the `frontend/` directory:
  
  ```bash
  cd ../frontend
  ```

- Install Node dependencies:
  
  ```bash
  npm install
  ```

---

## Configuration

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file (located at the root) with your credentials:

   ```ini
   GITHUB_TOKEN=your_github_personal_access_token
   FLASK_SECRET_KEY=your_secret_key
   ```

---

## Usage

### Running the Application

#### a. Backend Only

- In the `server/` directory, run:

  ```bash
  python app.py
  ```

#### b. Frontend Only

- In the `frontend/` directory, run:

  ```bash
  npm run dev
  ```

#### c. Run Both Together

- Use the provided script (from the project root):

  ```bash
  npm run dev:all
  ```

### Standalone GUI (Desktop)

- In the `server/` directory, run the GUI app:

  ```bash
  python gui.py
  ```

---

## How It Works

- **REST API (Flask):**  
  Exposes endpoints such as:
  - `GET /api/deployments?username=<>&repo=<>`  
  - `POST /api/deployments/<id>/mark_inactive?username=<>&repo=<>`  
  - `DELETE /api/deployments/<id>?username=<>&repo=<>`

- **Desktop GUI (Tkinter):**  
  - Enter GitHub username and repository name.
  - Click "List Deployments" to load all deployments.
  - Each row in the list displays two action buttons:
    - **Mark Inactive:** Marks the deployment as inactive. If already inactive, shows an info message.
    - **Delete:** Only clickable when the deployment is inactive.
  
- **Web Frontend (Next.js):**  
  Displays deployment information and uses the REST API for actions.

---

## Directory Structure

```plaintext
.
├── .env.example
├── .gitignore
├── frontend
│   ├── app
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components
│   │   ├── github-deployments.tsx
│   │   ├── theme-provider.tsx
│   │   └── ui
│   │       ├── badge.tsx
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── table.tsx
│   │       └── toast.tsx
│   ├── hooks
│   │   ├── use-mobile.tsx
│   │   └── use-toast.tsx
│   ├── lib
│   │   └── utils.tsx
│   ├── next.config.mjs
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── styles
│   │   └── globals.css
│   ├── tailwind.config.ts
│   ├── ts.config.json
│   └── tsconfig.json
├── LICENSE
├── README.md
└── server
    ├── app.py
    ├── gui.py
    └── requirements.txt
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
