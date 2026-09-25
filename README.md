# ApplyCM Monorepo

ApplyCM is a platform where Cameroonian students discover schools and apply to multiple schools with one shared profile.

## Directory Structure

*   `/frontend` - SvelteKit frontend app
*   `/backend` - Python FastAPI backend app
*   `/docs` - Architecture documentation (empty for now)

## Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure environment variables:
    ```bash
    cp .env.example .env
    # Edit .env with your local settings
    ```
5.  Apply database migrations:
    ```bash
    alembic upgrade head
    ```
6.  Run the application (the frontend expects port 8001):
    ```bash
    uvicorn app.main:app --reload --port 8001
    ```
7.  Run the tests (they use a throwaway SQLite database, no Neon needed):
    ```bash
    python -m pytest
    ```

### Deploying (Render + Neon)

New columns are added through Alembic migrations, so the migration must run
against Neon on every deploy. Set Render's **Build Command** to:

```bash
pip install -r requirements.txt && alembic upgrade head
```

### Application profile API

All routes need `Authorization: Bearer <token>` and act on the signed-in user.

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/api/students/me` | Full profile, including `completed_sections` (404 until first save) |
| `PUT` | `/api/students/me/{section}` | Save one wizard section: `profile`, `contact`, `education`, `testing`, `activities`, `writing` |

The first save of any section creates the profile. A section is complete once
all its required fields are stored. See
[docs/application-profile-walkthrough.md](docs/application-profile-walkthrough.md)
for how the wizard is wired to the database.

## Frontend Setup

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Configure environment variables:
    ```bash
    cp .env.example .env
    # Edit .env with your local settings
    ```
    `PUBLIC_API_BASE_URL` picks the backend. Without it, the frontend uses the
    deployed Render API (`https://applycm-backend.onrender.com`); the example
    file points to a local backend on port 8001.
4.  Run the development server:
    ```bash
    npm run dev
    ```
