from __future__ import annotations

from fastapi import FastAPI

from routes_data import router as data_router
from routes_health import router as health_router
from routes_ui import router as ui_router
from routes_vapi import router as vapi_router
from schemas_vapi import PhoneNumbersResponse, Settings
from service_vapi import VapiClient, get_settings, get_vapi_client


app = FastAPI(title='API')
app.include_router(health_router)
app.include_router(data_router)
app.include_router(ui_router)
app.include_router(vapi_router)
