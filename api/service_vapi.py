from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import httpx
from fastapi import Depends, HTTPException

from schemas_vapi import OutboundCallRequest, Settings


@lru_cache
def get_settings() -> Settings:
    return Settings(
        private_key=os.getenv('VAPI_PRIVATE_KEY'),
        default_phone_number=os.getenv('VAPI_DEFAULT_PHONE_NUMBER'),
        default_phone_number_id=os.getenv('VAPI_DEFAULT_PHONE_NUMBER_ID'),
        base_url=os.getenv('VAPI_BASE_URL', 'https://api.vapi.ai'),
    )


class VapiClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def get_assistant(self, assistant_id: str) -> dict[str, Any]:
        response = await self._request('GET', f'/assistant/{assistant_id}')
        if not isinstance(response, dict):
            raise HTTPException(status_code=502, detail='Unexpected assistant response from Vapi.')
        return response

    async def list_phone_numbers(self) -> list[dict[str, Any]]:
        response = await self._request('GET', '/phone-number')
        if isinstance(response, list):
            return [item for item in response if isinstance(item, dict)]
        if isinstance(response, dict):
            for key in ('items', 'results', 'data'):
                value = response.get(key)
                if isinstance(value, list):
                    return [item for item in value if isinstance(item, dict)]
        raise HTTPException(status_code=502, detail='Unexpected phone-number response from Vapi.')

    async def create_call(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = await self._request('POST', '/call', json=payload)
        if not isinstance(response, dict):
            raise HTTPException(status_code=502, detail='Unexpected call response from Vapi.')
        return response

    async def _request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        try:
            async with httpx.AsyncClient(
                base_url=self.settings.base_url,
                headers={'Authorization': f'Bearer {self.settings.private_key}'},
                timeout=30.0,
            ) as client:
                response = await client.request(method, path, json=json)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text or exc.response.reason_phrase
            raise HTTPException(
                status_code=502,
                detail=f'Vapi API error ({exc.response.status_code}): {detail}',
            ) from exc
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f'Vapi request failed: {exc}') from exc

        return response.json()


def get_vapi_client(settings: Settings = Depends(get_settings)) -> VapiClient:
    if not settings.private_key:
        raise HTTPException(status_code=500, detail='Missing VAPI_PRIVATE_KEY environment variable.')
    return VapiClient(settings)


def normalize_phone_number(number: str | None) -> str | None:
    if not number:
        return None
    return ''.join(char for char in number if char.isdigit() or char == '+')


async def resolve_phone_number_id(
    request: OutboundCallRequest,
    settings: Settings,
    vapi_client: VapiClient,
) -> str:
    if request.phone_number_id:
        return request.phone_number_id
    if settings.default_phone_number_id:
        return settings.default_phone_number_id
    if settings.default_phone_number:
        normalized_target = normalize_phone_number(settings.default_phone_number)
        for phone_number in await vapi_client.list_phone_numbers():
            if normalize_phone_number(phone_number.get('number')) == normalized_target:
                phone_number_id = phone_number.get('id')
                if isinstance(phone_number_id, str) and phone_number_id:
                    return phone_number_id
        raise HTTPException(
            status_code=400,
            detail=(
                'Configured VAPI_DEFAULT_PHONE_NUMBER was not found in Vapi: '
                f'{settings.default_phone_number}'
            ),
        )

    raise HTTPException(
        status_code=400,
        detail=(
            'phoneNumberId is required or configure '
            'VAPI_DEFAULT_PHONE_NUMBER_ID / VAPI_DEFAULT_PHONE_NUMBER.'
        ),
    )
