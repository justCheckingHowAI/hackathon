from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from hiring_packs_store import HiringPackStorageError, HiringPacksStore, get_hiring_packs_store
from schemas_hiring_packs import HiringPack


router = APIRouter(prefix='/hiring-packs', tags=['hiring-packs'])


@router.get('/{person_id}', response_model=HiringPack)
def get_hiring_pack(
    person_id: str,
    store: HiringPacksStore = Depends(get_hiring_packs_store),
) -> HiringPack:
    try:
        hiring_pack = store.load(person_id)
    except HiringPackStorageError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    if hiring_pack is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Hiring pack not found.')

    return hiring_pack


@router.put('/{person_id}', response_model=HiringPack)
def put_hiring_pack(
    person_id: str,
    payload: dict[str, Any],
    store: HiringPacksStore = Depends(get_hiring_packs_store),
) -> HiringPack:
    try:
        return store.save_demo_to_default_person()
    except HiringPackStorageError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
