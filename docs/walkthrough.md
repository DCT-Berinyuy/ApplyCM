# ApplyCM Monorepo - Developer Walkthrough

Welcome to the **ApplyCM** codebase! This document is designed for remote developers to quickly understand the monorepo structure, core design patterns, and module architecture. 

ApplyCM is a platform where Cameroonian students discover universities and apply to multiple programs using a single shared application profile.

---

## 📂 Repository Structure

The project is structured as a monorepo containing a SvelteKit frontend, a Python FastAPI backend, and architectural documentation.

```
/
├── docs/               # Architecture and walkthrough documentation
│   └── walkthrough.md  # This document
├── backend/            # Python FastAPI backend + SQLAlchemy + Alembic
├── frontend/           # SvelteKit (Svelte 5 runes + TypeScript)
├── .gitignore          # Global git ignore configurations
└── README.md           # Quick setup and run instructions
```

---

## 🐍 Backend Architecture (`/backend`)

The backend is built with Python 3.12+, using **FastAPI** for the API layer, **SQLAlchemy** for ORM database interactions, and **Alembic** for migrations.

### Core Folder Structure
```
backend/
├── app/
│   ├── core/           # Configuration and security logic
│   ├── db/             # Sessionmaker and declarative base
│   ├── models/         # SQLAlchemy ORM entities
│   ├── schemas/        # Pydantic validation schemas
│   ├── services/       # Core business logic handlers
│   ├── routers/        # Thin endpoint routers
│   ├── dependencies.py # FastAPI dependencies (db, auth state)
│   └── main.py         # Entrypoint, CORS settings, routers mount
├── alembic/            # Database migrations directory
├── alembic.ini         # Alembic configuration
├── requirements.txt    # Backend dependencies list
└── .env.example        # Environment variables template
```

### Key Design Patterns & Modules

1.  **Circular Import Protection (`app/db/base_class.py` & `app/db/base.py`)**:
    *   To prevent circular import loops between models during migration discovery, `Base` is defined inside [base_class.py](file:///home/dct/Desktop/Development/ApplyCM/backend/app/db/base_class.py).
    *   Models import `Base` from `base_class.py`.
    *   Alembic references [base.py](file:///home/dct/Desktop/Development/ApplyCM/backend/app/db/base.py), which imports `Base` and then imports all models so they register on the metadata object.
2.  **Configuration (`app/core/config.py`)**:
    *   Utilizes `pydantic-settings` to load configuration from the environment/`.env`.
    *   Uses Pydantic v2 `model_config` syntax for settings configuration.
3.  **Authentication (`app/core/security.py` & `app/dependencies.py`)**:
    *   Password hashing is stubbed using `passlib` context (`bcrypt`).
    *   `get_current_user` in `dependencies.py` acts as a secure FastAPI dependency. It is type-annotated with `-> User` and raises an `HTTPException` placeholder to prevent typing errors.
4.  **Database Entities (`app/models/`)**:
    *   `user.py`: Stores credential data.
    *   `student_profile.py`: Central entity containing shared student profile information.
    *   `school.py` & `program.py`: Universities and their respective curriculum.
    *   `application.py`: Tracks student program applications. Uses database-side timestamp defaults (`func.now()`).
    *   `favorite.py`: Join-table mapping user bookmarks to schools.
    *   `document.py`: PDF/image uploads related to student profiles.
5.  **Pydantic Schemas (`app/schemas/`)**:
    *   Mirror database models to validate incoming requests and serialize outgoing responses.
    *   Includes `BatchApplicationCreate` to support the **Apply-to-Many** logic, passing a single profile ID and a list of program IDs.
6.  **Services (`app/services/`)**:
    *   This is where all business logic resides. Avoid putting SQL queries or operations directly in routers. Keep routers thin.
    *   `application_service.py` contains the stub for `apply_to_multiple_programs()`.

---

## ⚡ Frontend Architecture (`/frontend`)

The frontend is built with **SvelteKit** using **Svelte 5 runes** (`$props`, `$state`, etc.) and fully configured with **TypeScript**.

### Core Folder Structure
```
frontend/
├── src/
│   ├── lib/
│   │   ├── api/        # Fetch client wrapper and API modules
│   │   ├── components/ # Reusable UI components
│   │   ├── stores/     # Svelte session and progress stores
│   │   └── types/      # TypeScript interfaces mirroring backend
│   ├── routes/         # Routing pages and Svelte layouts
│   ├── app.d.ts        # Global type definitions
│   └── app.html        # Shell HTML file
├── static/             # Static public assets (e.g. favicon.png)
├── svelte.config.js    # Svelte configuration
├── tsconfig.json       # TypeScript compiler settings
├── vite.config.ts      # Vite server configuration
├── package.json        # Node dependencies list
└── .env.example        # Frontend env variables template
```

### Key Modules & Routing Layout

1.  **Svelte 5 UI & Event Handling**:
    *   Forms use the modern Svelte 5 `onsubmit={(e) => e.preventDefault()}` event properties instead of the deprecated `on:submit` directives.
    *   Layouts render child routes using `let { children } = $props()` and `{@render children()}`.
2.  **API client Fetch Wrapper (`src/lib/api/client.ts`)**:
    *   Centralized request dispatcher that appends auth tokens to headers from the store.
3.  **Types (`src/lib/types/index.ts`)**:
    *   TypeScript interfaces mirror the backend schemas (`User`, `StudentProfile`, `School`, etc.) ensuring compile-time safety across boundaries.
4.  **Route Groups (`src/routes/`)**:
    *   **Unauthenticated group `(auth)`**: Subfolders `login` and `signup` contain layouts for user credential collection.
    *   **Authenticated dashboard group `(app)`**: Renders a shared sidebar/nav layout. Subpages:
        *   `dashboard/`: Displays summary statistics.
        *   `discover/`: Interactive school finder with batch selection support.
        *   `favorites/`: Saved listings.
        *   `settings/`: Account preferences.
        *   `application/`: Nested step-by-step profile wizard (`profile`, `education`, `writing`) with step layout and store tracking.

---

## 🔗 Frontend-Backend Integration

*   **API URL Configuration**: The frontend API module fetches data using the backend URL configured in `.env` (`PUBLIC_API_BASE_URL`).
*   **CORS Safeguard**: The FastAPI backend is configured to accept requests from the SvelteKit development server (`http://localhost:5173`) with credentials allowed (`allow_credentials=True`), preventing CORS errors during development.
