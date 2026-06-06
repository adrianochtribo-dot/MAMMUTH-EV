"""
MAMMUTH•EVENTS™ — Safety Engine
Module: main.py
Version: 1.0.0

FastAPI entrypoint — Safety Engine Scenario A.
Avvio: uvicorn main:app --reload --port 8001
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes.predict import router as predict_router

app = FastAPI(
    title="MAMMUTH•EVENTS™ — Safety Engine",
    description=(
        "Modulo predittivo per la sicurezza degli eventi di massa. "
        "Filosofia: INFORMARE, CONSIGLIARE, MITIGARE — mai vietare."
    ),
    version="1.0.0",
    contact={
        "name": "KREATIO UNIVERSAL SYSTEM™",
        "url": "https://github.com/adrianochtribo-dot/MAMMUTH-EV",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api/v1")


@app.get("/api/v1/safety/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "safety-engine",
        "scenario": "A",
        "version": "1.0.0",
    }
