from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Request

from schemas_vapi import (
    OutboundCallRequest,
    PhoneNumbersResponse,
    Settings,
    VapiToolWebhookResponse,
)
from service_vapi import (
    VapiClient,
    get_settings,
    get_vapi_client,
    resolve_assistant_id,
    resolve_phone_number_id,
)
from tools import run_cypher_query_tool, run_retrieve_rag_contexts_tool, run_whoami_tool


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
    return await run_whoami_tool(await request.body())


@router.post('/vapi/tools/run-cypher-query', response_model_exclude_none=True)
async def vapi_run_cypher_query_tool(
    request: Request,
) -> VapiToolWebhookResponse:
    return await run_cypher_query_tool(await request.body())


@router.post('/vapi/tools/retrieve-rag-contexts', response_model_exclude_none=True)
async def vapi_retrieve_rag_contexts_tool(
    request: Request,
) -> VapiToolWebhookResponse:
    return await run_retrieve_rag_contexts_tool(await request.body())
