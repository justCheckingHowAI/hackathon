from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from db import DatabaseConfigError, get_database


router = APIRouter(tags=['health'])


@router.get('/')
def read_root() -> RedirectResponse:
    return RedirectResponse(url='/ui', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/health')
def healthcheck() -> dict[str, str]:
    return {'status': 'ok'}


@router.get('/health/db')
def db_healthcheck() -> dict[str, str]:
    try:
        db = get_database()
        db.ping()
    except DatabaseConfigError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f'Database unavailable: {exc}') from exc

    return {'status': 'ok'}
