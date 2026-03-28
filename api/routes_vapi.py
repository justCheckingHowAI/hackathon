from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from schemas_vapi import OutboundCallRequest, PhoneNumbersResponse, Settings
from service_vapi import VapiClient, get_settings, get_vapi_client, resolve_phone_number_id


router = APIRouter(tags=['vapi'])


@router.get('/vapi/assistant/{assistant_id}')
async def get_vapi_assistant(
    assistant_id: str,
    vapi_client: VapiClient = Depends(get_vapi_client),
) -> dict[str, Any]:
    return await vapi_client.get_assistant(assistant_id)


@router.get('/vapi/phone-numbers')
async def get_vapi_phone_numbers(
    vapi_client: VapiClient = Depends(get_vapi_client),
) -> PhoneNumbersResponse:
    return PhoneNumbersResponse(items=await vapi_client.list_phone_numbers())


@router.post('/vapi/calls')
async def create_vapi_call(
    request: OutboundCallRequest,
    settings: Settings = Depends(get_settings),
    vapi_client: VapiClient = Depends(get_vapi_client),
) -> dict[str, Any]:
    phone_number_id = await resolve_phone_number_id(request, settings, vapi_client)

    customer: dict[str, Any] = {'number': request.customer_number}
    if request.customer_name:
        customer['name'] = request.customer_name

    payload = {
        'assistantId': request.assistant_id,
        'phoneNumberId': phone_number_id,
        'customer': customer,
    }
    return await vapi_client.create_call(payload)
