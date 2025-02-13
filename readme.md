# GitHub Deployment Cleaner (Flask + React)

This project provides a **GitHub Deployment Cleaner**, which helps manage and clean up GitHub deployments efficiently.

- **Frontend**: React + Tailwind CSS (Deployed on **Vercel**)
- **Backend**: Flask + GitHub API (Deployed on **Render**)
- **Database**: None (GitHub API used as storage)

---

## 🚀 Features

✔️ **List all deployments** in a GitHub repository  
✔️ **Mark deployments as inactive**  
✔️ **Delete outdated deployments**  
✔️ **Fully responsive frontend** (React + Tailwind)  
✔️ **Deployed with CI/CD** using **Render (Backend)** & **Vercel (Frontend)**

---

## 📂 Project Structure

```
📦 project-root
├── 📂 frontend/          # React (Vercel)
│   ├── 📂 components/ui  # UI Components (Badge, Button, etc.)
│   ├── 📄 github-deployments.tsx  # Main frontend component
│   ├── 📄 package.json   # Dependencies & scripts
│   ├── 📄 vite.config.ts # Vite Configuration
│   └── ...
│
├── 📂 github-deployment-cleaner/  # Flask (Render)
│   ├── 📄 app.py       # Flask API server
│   ├── 📄 github_deployments.py  # GitHub API interactions
│   ├── 📄 cli.py       # CLI tool for managing deployments
│   ├── 📄 requirements.txt # Python dependencies
│   └── ...
│
└── 📄 README.md
```

---

## 🔧 Setup Guide (Local Development)

### **1️⃣ Backend (Flask on Render)**

#### ✅ **Step 1: Clone the Repo & Install Dependencies**

```bash
git clone https://github.com/your-username/github-deployment-cleaner.git
cd github-deployment-cleaner
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### ✅ **Step 2: Set Up Environment Variables**

Create a `.env` file inside `github-deployment-cleaner/`:

```ini
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_USER=your_github_username
GITHUB_REPO=your_github_repo_name
FLASK_SECRET_KEY=your_secret_key
```

#### ✅ **Step 3: Run the Backend**

```bash
python app.py
```

Flask server runs at **http://127.0.0.1:5000**.

---

### **2️⃣ Frontend (React on Vercel)**

#### ✅ **Step 1: Install Dependencies**

```bash
cd ../frontend
npm install
```

#### ✅ **Step 2: Start Development Server**

```bash
npm run dev  # Or npx vite
```

Frontend runs at **http://localhost:5173**.

---

## 🚀 Deployment Guide

### **Deploy Backend on Render**

1. Go to **Render** ([https://render.com](https://render.com))
2. Create a **New Web Service**
3. Connect your GitHub repository
4. Set **Build Command**:
   ```bash
   pip install -r requirements.txt
   ```
5. Set **Start Command**:
   ```bash
   gunicorn app:app
   ```
6. Add **Environment Variables** (from `.env` file)
7. Deploy & get backend URL (e.g., `https://your-app.onrender.com`)

---

### **Deploy Frontend on Vercel**

1. Go to **Vercel** ([https://vercel.com](https://vercel.com))
2. Connect your GitHub repository
3. Set **Build Command**:
   ```bash
   npm install && npm run build
   ```
4. Set **Environment Variables**
5. Deploy & get frontend URL (e.g., `https://your-app.vercel.app`)

---

## 🛠️ API Endpoints

| Method | Endpoint                              | Description                 |
| ------ | ------------------------------------- | --------------------------- |
| GET    | `/api/deployments`                    | Fetch all deployments       |
| POST   | `/api/deployments/<id>/mark_inactive` | Mark deployment as inactive |
| DELETE | `/api/deployments/<id>`               | Delete a deployment         |

---

## 📜 License

This project is open-source under the **MIT License**.

---

## 🌟 Contributions

Feel free to fork, submit PRs, or suggest improvements!
