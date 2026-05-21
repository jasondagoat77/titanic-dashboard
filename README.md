# 🚢 Titanic Survival Dashboard

> Full-stack data analysis app — Pandas × Matplotlib × Flask × React (Vite) × Docker × Render

---

## Architecture

```
titanic-dashboard/
├── backend/              # Flask API + Pandas analysis + Matplotlib charts
│   ├── app.py            # REST API (5 endpoints)
│   ├── generate_charts.py# Matplotlib chart generation (6 charts)
│   ├── titanic.csv       # Kaggle Titanic dataset
│   ├── stats.json        # Pre-computed statistics
│   ├── static/charts/    # Generated PNG charts served statically
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Vite + React dashboard
│   ├── src/
│   │   ├── App.jsx               # Root layout + navigation
│   │   ├── components/
│   │   │   ├── StatCard.jsx      # KPI metric cards
│   │   │   ├── ChartGrid.jsx     # Zoomable chart gallery
│   │   │   ├── SurvivalMatrix.jsx# Class × Gender heatmap
│   │   │   └── DataTable.jsx     # Paginated raw data table
│   │   └── index.css             # CSS variables + reset
│   ├── vite.config.js    # Proxy to Flask in dev
│   ├── nginx.conf        # Nginx config for production
│   └── Dockerfile
├── docker-compose.yml    # Local full-stack with one command
└── render.yaml           # Render.com deployment config
```

## Tech Stack

| Layer      | Technology               | Purpose                          |
|------------|--------------------------|----------------------------------|
| Data       | Pandas 2.x               | Load, clean, aggregate CSV       |
| Charts     | Matplotlib + Seaborn     | 6 pre-rendered analysis charts   |
| Backend    | Flask 3 + Gunicorn       | REST API serving data + charts   |
| Frontend   | React 18 + Vite 5        | SPA dashboard with 4 tabs        |
| Styling    | CSS Modules              | Scoped styles, dark editorial UI |
| Container  | Docker + Compose         | Reproducible local environment   |
| Deploy     | Render.com               | Free-tier cloud hosting          |

---

## Local Development

### Option A — Docker Compose (recommended)

```bash
# 1. Clone / enter directory
cd titanic-dashboard

# 2. Start everything
docker-compose up --build

# 3. Open browser
open http://localhost         # React frontend
open http://localhost:5000/health  # Flask health check
```

### Option B — Run services separately

**Backend (Flask)**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python generate_charts.py       # Pre-render charts
python app.py                   # Starts on :5000
```

**Frontend (Vite + React)**

```bash
cd frontend
npm install
npm run dev                     # Starts on :5173, proxies /api → :5000
```

---

## API Endpoints

| Method | Path                            | Returns                               |
|--------|---------------------------------|---------------------------------------|
| GET    | `/health`                       | `{status: "ok", rows: 891}`          |
| GET    | `/api/stats`                    | Summary statistics JSON               |
| GET    | `/api/charts`                   | Chart metadata + URLs                 |
| GET    | `/api/data/sample`              | First 20 rows + column names          |
| GET    | `/api/data/survived-by-class-sex` | Cross-tabulation for matrix view    |
| GET    | `/static/charts/<name>.png`     | Matplotlib chart PNG                  |

---

## Charts Generated (Matplotlib)

1. **Survival by Passenger Class** — Grouped bar chart (1st / 2nd / 3rd)
2. **Age Distribution by Survival** — Overlapping histograms
3. **Survival Rate by Gender** — Bar chart (63.8% F vs 20.0% M)
4. **Fare Distribution** — Log-scale histogram by outcome
5. **Survival by Port of Embarkation** — Southampton / Cherbourg / Queenstown
6. **Feature Correlation Heatmap** — Seaborn heatmap of all numeric features

---

## Deploy to Render.com

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial: Titanic full-stack dashboard"
git remote add origin https://github.com/YOUR_USER/titanic-dashboard.git
git push -u origin main
```

### Step 2 — Connect to Render

1. Go to [render.com](https://render.com) → **New → Blueprint**
2. Connect your GitHub repo
3. Render auto-detects `render.yaml` and creates **two services**:
   - `titanic-backend` (Flask on port 5000)
   - `titanic-frontend` (React + nginx on port 80)

### Step 3 — Update backend URL in render.yaml

After the first deploy, copy your backend's Render URL (e.g. `https://titanic-backend.onrender.com`), then update `render.yaml`:

```yaml
- key: VITE_API_URL
  value: "https://titanic-backend.onrender.com"
```

Push the change → Render auto-redeploys.

### Step 4 — Also update nginx.conf (optional)

For a fully self-contained frontend, update the proxy in `nginx.conf`:

```nginx
location /api/ {
    proxy_pass https://titanic-backend.onrender.com;
}
```

---

## Environment Variables

| Variable       | Service  | Default  | Description                     |
|----------------|----------|----------|---------------------------------|
| `PORT`         | Backend  | `5000`   | Flask/Gunicorn listen port      |
| `VITE_API_URL` | Frontend | `""`     | Backend base URL (empty = proxy)|

---

## Dataset

**Titanic: Machine Learning from Disaster** — Kaggle  
891 passengers · 9 features: PassengerId, Survived, Pclass, Sex, Age, SibSp, Parch, Fare, Embarked

Key findings:
- Overall survival rate: **35.5%**
- Female survival: **63.8%** · Male survival: **20.0%**
- 1st class: **57.6%** · 2nd class: **51.5%** · 3rd class: **20.2%**
- Average fare: **£32.11** · Average age: **29.9 years**
