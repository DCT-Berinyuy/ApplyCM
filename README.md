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
5.  Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

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
4.  Run the development server:
    ```bash
    npm run dev
    ```
