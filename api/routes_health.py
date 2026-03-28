from __future__ import annotations

from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse


router = APIRouter(tags=['health'])


@router.get('/')
def read_root() -> RedirectResponse:
    return RedirectResponse(url='/ui', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/health')
def healthcheck() -> dict[str, str]:
    return {'status': 'ok'}
