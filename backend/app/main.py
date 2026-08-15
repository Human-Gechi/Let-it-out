from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import health, prompts, reflect

app = FastAPI(title="Let It Out API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router)
app.include_router(prompts.router)
app.include_router(reflect.router)
