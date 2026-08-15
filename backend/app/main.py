from fastapi import FastAPI
from backend.app.routers import health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Let It Out API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(health.router)