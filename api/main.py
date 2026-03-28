from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes_health import router as health_router
from routes_hiring_packs import router as hiring_packs_router
from routes_vapi import router as vapi_router
from routes_vectorize import router as vectorize_router
from schemas_vapi import PhoneNumbersResponse, Settings
from service_vapi import VapiClient, get_settings, get_vapi_client
from taskiq_broker import broker


@asynccontextmanager
async def lifespan(_: FastAPI):
    await broker.startup()
    try:
        yield
    finally:
        await broker.shutdown()


app = FastAPI(title='API', lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://127.0.0.1:8000',
        'http://localhost:8000',
        'http://127.0.0.1:5173',
        'http://localhost:5173',
        'https://app.gemellus.app',
        '*',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(health_router)
app.include_router(hiring_packs_router)
app.include_router(vapi_router)
app.include_router(vectorize_router)
