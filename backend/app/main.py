from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import health, prompts, reflect

app = FastAPI(
    title="Let It Out API",
    description="A backend API for the Let It Out app.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Let It Out API",
        "docs": "/docs",
        "health": "/health",
    }


app.include_router(health.router)
app.include_router(prompts.router)
app.include_router(reflect.router)
