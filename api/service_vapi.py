from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from fastapi import Depends, HTTPException
from vapi import AsyncVapi
from vapi.core.api_error import ApiError

from schemas_vapi import OutboundCallRequest, Settings


@lru_cache
def get_settings() -> Settings:
    return Settings(
        private_key=os.getenv('VAPI_PRIVATE_KEY'),
        assistant_id=os.getenv('VAPI_ASSISTANT_ID'),
        default_phone_number=os.getenv('VAPI_DEFAULT_PHONE_NUMBER'),
        default_phone_number_id=os.getenv('VAPI_DEFAULT_PHONE_NUMBER_ID'),
        base_url=os.getenv('VAPI_BASE_URL', 'https://api.vapi.ai'),
    )


def serialize_vapi_model(value: Any) -> Any:
    if hasattr(value, 'model_dump'):
        return value.model_dump(mode='json', by_alias=True, exclude_none=True)
    if isinstance(value, list):
        return [serialize_vapi_model(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize_vapi_model(item) for key, item in value.items()}
    return value


def camel_to_snake(name: str) -> str:
    chars: list[str] = []
    for char in name:
        if char.isupper():
            chars.extend(['_', char.lower()])
        else:
            chars.append(char)
    return ''.join(chars)


def prepare_assistant_update_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {camel_to_snake(key): value for key, value in payload.items()}


class VapiClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = AsyncVapi(
            token=settings.private_key,
            base_url=settings.base_url,
            timeout=30.0,
        )

    async def get_assistant(self, assistant_id: str) -> dict[str, Any]:
        try:
            assistant = await self.client.assistants.get(assistant_id)
        except ApiError as exc:
            self._raise_api_error(exc)
        payload = serialize_vapi_model(assistant)
        if not isinstance(payload, dict):
            raise HTTPException(status_code=502, detail='Unexpected assistant response from Vapi.')
        return payload

    async def list_phone_numbers(self) -> list[dict[str, Any]]:
        try:
            phone_numbers = await self.client.phone_numbers.list()
        except ApiError as exc:
            self._raise_api_error(exc)
        payload = serialize_vapi_model(phone_numbers)
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        raise HTTPException(status_code=502, detail='Unexpected phone-number response from Vapi.')

    async def create_call(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            call = await self.client.calls.create(
                assistant_id=payload.get('assistantId'),
                phone_number_id=payload.get('phoneNumberId'),
                customer=payload.get('customer'),
            )
        except ApiError as exc:
            self._raise_api_error(exc)
        response = serialize_vapi_model(call)
        if not isinstance(response, dict):
            raise HTTPException(status_code=502, detail='Unexpected call response from Vapi.')
        return response

    async def update_assistant(self, assistant_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            assistant = await self.client.assistants.update(
                assistant_id,
                **prepare_assistant_update_payload(payload),
            )
        except ApiError as exc:
            self._raise_api_error(exc)
        response = serialize_vapi_model(assistant)
        if not isinstance(response, dict):
            raise HTTPException(status_code=502, detail='Unexpected assistant response from Vapi.')
        return response

    @staticmethod
    def _raise_api_error(exc: ApiError) -> None:
        status_code = exc.status_code or 502
        body = exc.body if exc.body is not None else str(exc)
        raise HTTPException(
            status_code=502,
            detail=f'Vapi API error ({status_code}): {body}',
        ) from exc


def get_vapi_client(settings: Settings = Depends(get_settings)) -> VapiClient:
    if not settings.private_key:
        raise HTTPException(status_code=500, detail='Missing VAPI_PRIVATE_KEY environment variable.')
    return VapiClient(settings)


def normalize_phone_number(number: str | None) -> str | None:
    if not number:
        return None
    return ''.join(char for char in number if char.isdigit() or char == '+')


def resolve_assistant_id(request: OutboundCallRequest, settings: Settings) -> str:
    if request.assistant_id:
        return request.assistant_id
    if settings.assistant_id:
        return settings.assistant_id
    raise HTTPException(
        status_code=400,
        detail='assistantId is required or configure VAPI_ASSISTANT_ID.',
    )


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
