from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from schemas_vapi import (
    OutboundCallRequest,
    PhoneNumbersResponse,
    Settings,
    VapiToolResult,
    VapiToolWebhookRequest,
    VapiToolWebhookResponse,
)
from service_vapi import (
    VapiClient,
    get_settings,
    get_vapi_client,
    resolve_assistant_id,
    resolve_phone_number_id,
)


router = APIRouter(tags=['vapi'])

WHOAMI_RESULT = (
    'You are Mike Grabowski, CTO & Founder at Callstack. '
    'Public profile: https://www.callstack.com/team/mike-grabowski'
)


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
    assistant_id = resolve_assistant_id(request, settings)
    phone_number_id = await resolve_phone_number_id(request, settings, vapi_client)

    customer: dict[str, Any] = {'number': request.customer_number}
    if request.customer_name:
        customer['name'] = request.customer_name

    payload = {
        'assistantId': assistant_id,
        'phoneNumberId': phone_number_id,
        'customer': customer,
    }
    return await vapi_client.create_call(payload)


@router.post('/vapi/tools/whoami', response_model_exclude_none=True)
async def vapi_whoami_tool(
    request: VapiToolWebhookRequest,
) -> VapiToolWebhookResponse:
    results: list[VapiToolResult] = []

    for tool_call in request.message.tool_call_list:
        if tool_call.name != 'whoami':
            results.append(
                VapiToolResult(
                    toolCallId=tool_call.id,
                    error=f'Unsupported tool call for this endpoint: {tool_call.name}',
                )
            )
            continue

        results.append(
            VapiToolResult(
                toolCallId=tool_call.id,
                result=WHOAMI_RESULT,
            )
        )

    return VapiToolWebhookResponse(results=results)
