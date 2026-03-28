from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, Request

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
    request: Request,
) -> VapiToolWebhookResponse:
    try:
        payload = json.loads((await request.body()).decode('utf-8') or '{}')
    except (UnicodeDecodeError, json.JSONDecodeError):
        return VapiToolWebhookResponse(results=[])

    def extract_tool_call_ids(value: Any) -> list[str]:
        if isinstance(value, dict):
            tool_calls = value.get('toolCallList')
            if isinstance(tool_calls, list):
                ids = [
                    tool_call.get('id')
                    for tool_call in tool_calls
                    if isinstance(tool_call, dict) and isinstance(tool_call.get('id'), str)
                ]
                if ids:
                    return ids

            tool_with_calls = value.get('toolWithToolCallList')
            if isinstance(tool_with_calls, list):
                ids = [
                    tool_call.get('toolCall', {}).get('id')
                    for tool_call in tool_with_calls
                    if isinstance(tool_call, dict)
                    and isinstance(tool_call.get('toolCall'), dict)
                    and isinstance(tool_call.get('toolCall', {}).get('id'), str)
                ]
                if ids:
                    return ids

            for nested_value in value.values():
                ids = extract_tool_call_ids(nested_value)
                if ids:
                    return ids

        if isinstance(value, list):
            for nested_value in value:
                ids = extract_tool_call_ids(nested_value)
                if ids:
                    return ids

        return []

    tool_call_ids = extract_tool_call_ids(payload)
    results = [
        VapiToolResult(
            toolCallId=tool_call_id,
            result=WHOAMI_RESULT,
        )
        for tool_call_id in tool_call_ids
    ]

    return VapiToolWebhookResponse(results=results)
