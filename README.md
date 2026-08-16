# Let It Out — Don't Hold Back

A private unsent-letter experience built for the **CS-Girlies Hackathon 2026** wellness track.

> **Research-backed approach:** Harvard Health research shows that [writing about emotions may ease stress and trauma](https://www.health.harvard.edu/healthbeat/writing-about-emotions-may-ease-stress-and-trauma). Let It Out is built on this principle—giving you a private space to write what you need to say.

Let It Out is a calm, reflective writing space for people who need somewhere to put difficult words without sending them. It is designed around expressive writing, gentle reflection, and intentional release.

---

## Table of Contents

- [Overview](#overview)
- [Why this project exists](#why-this-project-exists)
- [Core experience](#core-experience)
- [How the flow works](#how-the-flow-works)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Frontend](#frontend)
- [Backend](#backend)
- [Safety and wellness design](#safety-and-wellness-design)
- [Privacy model](#privacy-model)
- [Setup](#setup)
- [Environment variables](#environment-variables)
- [Running locally](#running-locally)
- [Testing](#testing)
- [Deployment notes](#deployment-notes)
- [Accessibility notes](#accessibility-notes)
- [Built By](#built-by)
---

## Overview

Let It Out is a web app for unsent letters.

It gives users a private place to:

1. choose who the letter is for,
2. write freely,
3. request a reflection,
4. and release the letter intentionally.

The app is built as a wellness tool, not a social platform. There are no accounts, no public posting, and no audience beyond the person writing.

---

## Why this project exists

Some feelings are easier to process when they are written down first.

This project was created around a simple idea:

- writing helps people name what they feel,
- a short reflection can help them feel understood,
- and a deliberate release can create a sense of closure.

The tone of the app is soft, private, and supportive. It is meant to feel like a safe place to put words that are too heavy, too honest, or too difficult to send.

---

## Core experience

### Writing
- A dedicated letter-writing space.
- Autosave in the browser.
- Recipient selection for different kinds of unsent letters.
- Character limit protection.
- Calm, paper-like visual styling.

### Reflection
- The user can request a reflection on their letter.
- If AI is enabled, a short response is generated.
- The reflection is warm, brief, and specific to the emotional tone of the letter.
- If AI is unavailable, the system falls back to a local message.

### Release
- If the user requests a reflection, the reflection is generated and the letter is sent into the void as part of the release moment.
- If the user does not request a reflection, they are prompted to hold the send button so the final action feels intentional.
- The release clears the draft from the browser.

### Safety
- The app checks for risk indicators in the text.
- If a safety concern is detected, the normal flow is interrupted and crisis support resources are shown.

---

## How the flow works

1. The user opens the writing page.
2. They begin an unsent letter.
3. They may request a reflection.
4. If a reflection is requested, the app generates a short reflection and then releases the letter into the void.
5. If no reflection is requested, the app asks the user to hold the send button so the final action feels deliberate.
6. The draft is then cleared from local storage.

This flow was designed to feel intentional rather than impulsive.

---

## Tech stack

| Layer | Tools |
| --- | --- |
| Backend | Python, FastAPI, Pydantic |
| AI / LLM | Groq API, optional AI reflections and prompts |
| Frontend | Nuxt 4, Vue 3, TypeScript |
| Styling | Tailwind CSS, custom CSS |
| Icons | Lucide |
| Testing | Pytest |
| Linting | Ruff |
| State / Storage | Browser local storage |
| Runtime / Dev Tools | Node.js, npm |

---

## Project structure

```text
backend/
  app/
    main.py
    config.py
    schemas.py
    prompts/
      system_prompts.py
      user_prompts.json
    routers/
      health.py
      prompts.py
      reflect.py
    services/
      ai_client.py
      ratelimit.py
      safety.py
  tests/
    test_health.py
    test_reflect.py

frontend/
  nuxt.config.ts
  app/
    assets/css/main.css
    composables/
      useLetItOutApi.ts
      useLetterDraft.ts
      useTheme.ts
    components/
      CrisisCard.vue
      HealthPill.vue
      InkFlourish.vue
      PromptCard.vue
      RecipientPicker.vue
      ReflectionPanel.vue
      ReleaseRitual.vue
      SiteFooter.vue
      SiteHeader.vue
      ThemeMenu.vue
      Wordmark.vue
    data/
      recipients.ts
    pages/
      index.vue
      write.vue
      about.vue
      [...slug].vue
```

---

## Frontend

The frontend is where the writing experience lives.

### Main pages
- `frontend/app/pages/index.vue`
- `frontend/app/pages/write.vue`
- `frontend/app/pages/about.vue`

### Key frontend behaviors
- draft autosave
- prompt loading
- reflection request handling
- release ritual interaction
- theme persistence
- backend health checks

### Main frontend composables
- `useLetterDraft`
- `useLetItOutApi`
- `useTheme`

### Main frontend components
- `ReflectionPanel`
- `ReleaseRitual`
- `RecipientPicker`
- `CrisisCard`
- `HealthPill`

---

## Backend

The backend is a FastAPI service that supports prompts, reflections, health checks, and safety-aware responses.

### Main backend files
- `backend/app/main.py` — Entry point. Sets up FastAPI app, CORS, and routes.
- `backend/app/config.py` — Configuration management. Reads environment variables and exposes settings.
- `backend/app/schemas.py` — Pydantic models. Defines request/response data structures.
- `backend/app/routers/prompts.py` — Prompt endpoint. Retrieves writing prompts by recipient type.
- `backend/app/routers/reflect.py` — Reflection endpoint. Generates AI reflections on letter text.
- `backend/app/routers/health.py` — Health check endpoint. Reports backend and AI service status.
- `backend/app/services/ai_client.py` — AI integration. Handles calls to Groq API and fallback logic.
- `backend/app/services/safety.py` — Safety scanning. Detects risk indicators and self-harm language.

### API endpoints

#### `GET /`
Returns a basic welcome response.

#### `GET /health`
Returns backend and AI status information.

#### `GET /prompt?recipient_type=...`
Returns a short writing prompt for the selected recipient type.

#### `POST /reflect`
Accepts letter text and returns a short reflection.

---

## Safety and wellness design

Let It Out is a wellness project, but it is **not** a crisis service.

### Safety approach
The app scans for high-risk language and self-harm indicators. If risk is detected:

- the usual flow is interrupted,
- a crisis message is shown,
- and support resources are displayed instead of continuing normally.

### Why this matters
The app is meant to support emotional expression, but it should not replace real support, emergency care, or therapy.

### Crisis resources
Crisis support is surfaced in the UI through the crisis card and footer.

---

## Privacy model

The app is intentionally private.

### Stored locally in the browser
- Draft letters
- Theme preference
- Writing state

### Sent to the backend only when needed
- Letter text for reflection
- Letter text for prompt-related processing

### Not included
- No user accounts
- No public feed
- No social posting
- No permanent server-side draft storage

This keeps the experience lightweight and personal.

---

## Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- npm

### Clone the repository
```powershell
git clone <repo-url>
cd let-it-out
```

### Backend setup
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend setup
```powershell
cd frontend
npm install
```

---

## Environment variables

### Backend
These are used by `backend/app/config.py`.

| Variable | Purpose | Default |
| --- | --- | --- |
| `AI_ENABLED` | Enables AI-powered prompts and reflections | `true` |
| `AI_API_KEY` | API key for the AI provider | empty |
| `AI_PROVIDER` | AI provider name | `groq` |
| `AI_MODEL` | Model name | `llama-3.3-70b-versatile` |
| `ALLOWED_ORIGINS` | CORS allowlist | `http://127.0.0.1:3000,http://localhost:3000` |
| `REQUEST_TIMEOUT_SECONDS` | API timeout | `15` |
| `APP_NAME` | Application name | Let It Out |
| `ENVIRONMENT` | Environment label | `Production` |

### Frontend
These are used by Nuxt runtime config.

| Variable | Purpose | Default |
| --- | --- | --- |
| `NUXT_PUBLIC_API_BASE` | Backend base URL | `http://127.0.0.1:8000` |

---

## Running locally

### Start the backend
From the repository root:

```powershell
venv\Scripts\uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

### Start the frontend
In a second terminal:

```powershell
cd frontend
npm run dev -- --host 127.0.0.1 --port 3000
```

---

## Testing

### Backend tests
From the repository root:

```powershell
cd backend
pytest
```

### Frontend checks
From the repository root:

```powershell
cd frontend
npm run lint
```

If frontend tests are added later, they should be documented here as well.

---

## Deployment notes

### Backend deployment on Render

1. Create a new Web Service on Render.
2. Connect your repository.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`.
5. Add all backend environment variables in Render's environment settings.
6. Deploy. Render will assign a URL like `https://your-app-name.onrender.com`.

### Frontend deployment on Vercel

1. Import your repository into Vercel.
2. Set the root directory to `frontend`.
3. Set the build output directory to `.output/public`.
4. Add the environment variable:
   - `NUXT_PUBLIC_API_BASE` = `https://your-app-name.onrender.com` (your Render backend URL)
5. Deploy. Vercel will assign a URL like `https://your-app-name.vercel.app`.

### Post-deployment

- Update the backend `ALLOWED_ORIGINS` to include your Vercel frontend URL.
- Test the full flow (writing, reflection, release) across both deployments.

---

## Accessibility notes

Let It Out is designed to be calm and usable for as many people as possible.

- Keyboard-friendly interactions
- Clear focus states
- Semantic headings and labels
- High-contrast theme options
- Reduced-motion-friendly UI patterns
- Short, readable feedback text

Accessibility should stay a core design requirement, not an afterthought.

---

## Built by

| Role | Name |
| --- | --- |
| Backend | Ogechukwu Okoli |
| Frontend & Deployment | Mayowa Akinyele |
