from __future__ import annotations

import json
import os
import subprocess
from base64 import b64encode
from functools import lru_cache
from typing import Any
from urllib import error, parse, request

from schemas_vapi import VapiToolResult, VapiToolWebhookResponse


WHOAMI_RESULT = json.dumps(
    {
        'person_id': 'mike',
        'full_name': 'Mike Grabowski',
        'role': 'CTO & Founder at Callstack',
        'public_profile': 'https://www.callstack.com/team/mike-grabowski',
        'summary': (
            'You are Mike Grabowski, CTO & Founder at Callstack. '
            'Public profile: https://www.callstack.com/team/mike-grabowski'
        ),
    }
)

def _decode_payload(raw_body: bytes) -> Any:
    try:
        return json.loads(raw_body.decode('utf-8') or '{}')
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}


def _extract_tool_calls(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        tool_calls = value.get('toolCallList')
        if isinstance(tool_calls, list):
            calls = [
                {
                    'id': tool_call.get('id'),
                    'arguments': tool_call.get('arguments', {}),
                }
                for tool_call in tool_calls
                if isinstance(tool_call, dict) and isinstance(tool_call.get('id'), str)
            ]
            if calls:
                return calls

        tool_with_calls = value.get('toolWithToolCallList')
        if isinstance(tool_with_calls, list):
            calls = []
            for item in tool_with_calls:
                if not isinstance(item, dict):
                    continue
                tool_call = item.get('toolCall')
                if not isinstance(tool_call, dict):
                    continue
                tool_call_id = tool_call.get('id')
                if not isinstance(tool_call_id, str):
                    continue
                calls.append(
                    {
                        'id': tool_call_id,
                        'arguments': tool_call.get('arguments', {}),
                    }
                )
            if calls:
                return calls

        for nested_value in value.values():
            calls = _extract_tool_calls(nested_value)
            if calls:
                return calls

    if isinstance(value, list):
        for nested_value in value:
            calls = _extract_tool_calls(nested_value)
            if calls:
                return calls

    return []


def _success_result(tool_call_id: str, result: Any) -> VapiToolResult:
    return VapiToolResult(toolCallId=tool_call_id, result=result)


def _error_result(tool_call_id: str, error_message: str) -> VapiToolResult:
    return VapiToolResult(toolCallId=tool_call_id, error=error_message)


async def run_whoami_tool(raw_body: bytes) -> VapiToolWebhookResponse:
    payload = _decode_payload(raw_body)
    tool_calls = _extract_tool_calls(payload)
    return VapiToolWebhookResponse(
        results=[_success_result(tool_call['id'], WHOAMI_RESULT) for tool_call in tool_calls]
    )


def _ensure_read_only_cypher(query: str) -> None:
    upper = query.upper()
    blocked = ['CREATE', 'MERGE', 'DELETE', 'SET ', 'REMOVE ', 'CALL ', 'DROP', 'LOAD CSV']
    if any(keyword in upper for keyword in blocked):
        raise ValueError('Only read-only Cypher queries are allowed.')


def _neo4j_request(url: str, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
    data = json.dumps(payload).encode('utf-8')
    req = request.Request(url, data=data, headers=headers, method='POST')
    try:
        with request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'Neo4j HTTP error {exc.code}: {body}') from exc
    except error.URLError as exc:
        raise RuntimeError(f'Neo4j request failed: {exc.reason}') from exc


def run_cypher_query(query: str, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
    neo4j_url = os.getenv('NEO4J_URL', 'http://70.34.249.162:7474')
    neo4j_username = os.getenv('NEO4J_USERNAME', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD')
    if not neo4j_password:
        raise RuntimeError('Missing NEO4J_PASSWORD environment variable.')

    _ensure_read_only_cypher(query)

    auth_raw = f'{neo4j_username}:{neo4j_password}'.encode('utf-8')
    auth = b64encode(auth_raw).decode('ascii')
    endpoint = f"{neo4j_url.rstrip('/')}/db/neo4j/tx/commit"
    payload = _neo4j_request(
        endpoint,
        {
            'statements': [
                {
                    'statement': query,
                    'parameters': parameters or {},
                }
            ]
        },
        {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {auth}',
        },
    )

    if payload.get('errors'):
        message = payload['errors'][0].get('message', 'Unknown Neo4j query error.')
        raise RuntimeError(f'Neo4j query error: {message}')

    result = (payload.get('results') or [{}])[0]
    rows = result.get('data') or []
    return {
        'columns': result.get('columns') or [],
        'rowCount': len(rows),
        'rows': [entry.get('row', entry) for entry in rows if isinstance(entry, dict)],
    }


async def run_cypher_query_tool(raw_body: bytes) -> VapiToolWebhookResponse:
    payload = _decode_payload(raw_body)
    tool_calls = _extract_tool_calls(payload)
    results: list[VapiToolResult] = []

    for tool_call in tool_calls:
        args = tool_call.get('arguments')
        if not isinstance(args, dict):
            results.append(_error_result(tool_call['id'], 'Tool arguments must be an object.'))
            continue

        query = args.get('query')
        parameters = args.get('parameters', {})

        if not isinstance(query, str) or not query.strip():
            results.append(_error_result(tool_call['id'], 'Missing query argument.'))
            continue
        if not isinstance(parameters, dict):
            results.append(_error_result(tool_call['id'], 'parameters must be an object.'))
            continue

        try:
            result = run_cypher_query(query, parameters)
        except (RuntimeError, ValueError) as exc:
            results.append(_error_result(tool_call['id'], str(exc)))
            continue

        results.append(_success_result(tool_call['id'], result))

    return VapiToolWebhookResponse(results=results)


def get_google_access_token() -> str:
    access_token = os.getenv('GOOGLE_ACCESS_TOKEN') or os.getenv('GCP_ACCESS_TOKEN')
    if access_token:
        return access_token

    try:
        return subprocess.check_output(
            ['gcloud', 'auth', 'print-access-token'],
            stderr=subprocess.STDOUT,
            text=True,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        detail = getattr(exc, 'output', None) or str(exc)
        raise RuntimeError(
            'Failed to get Google access token. Set GOOGLE_ACCESS_TOKEN or run '
            f"'gcloud auth print-access-token'. {detail.strip()}"
        ) from exc


def _vertex_request(url: str, method: str = 'GET', payload: dict[str, Any] | None = None) -> dict[str, Any]:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_google_access_token()}',
    }
    data = None if payload is None else json.dumps(payload).encode('utf-8')
    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'Vertex API error {exc.code}: {body}') from exc
    except error.URLError as exc:
        raise RuntimeError(f'Vertex request failed: {exc.reason}') from exc


def get_rag_base_url() -> str:
    project_id = os.getenv('GCP_PROJECT_ID', 'custom-helix-491611-k3')
    location = os.getenv('GCP_LOCATION', 'europe-west2')
    return f'https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}'


def list_rag_corpora(page_token: str | None = None) -> dict[str, Any]:
    url = f'{get_rag_base_url()}/ragCorpora'
    if page_token:
        url = f'{url}?{parse.urlencode({"pageToken": page_token})}'
    return _vertex_request(url, method='GET')


@lru_cache
def resolve_rag_corpus_name() -> str:
    corpus_name = os.getenv('VERTEX_RAG_CORPUS_NAME', 'gemelius corpus')
    if not corpus_name:
        raise RuntimeError('Missing VERTEX_RAG_CORPUS_NAME environment variable.')
    if corpus_name.startswith('projects/'):
        return corpus_name

    page_token: str | None = None
    while True:
        payload = list_rag_corpora(page_token)
        for corpus in payload.get('ragCorpora', []):
            if not isinstance(corpus, dict):
                continue
            display_name = corpus.get('displayName') or corpus.get('display_name')
            if display_name == corpus_name:
                name = corpus.get('name')
                if isinstance(name, str) and name:
                    return name

        page_token = payload.get('nextPageToken')
        if not isinstance(page_token, str) or not page_token:
            break

    raise RuntimeError(f"Could not find RAG corpus '{corpus_name}'.")


def retrieve_rag_contexts(query: str) -> dict[str, Any]:
    rag_corpus = resolve_rag_corpus_name()
    top_k = int(os.getenv('VERTEX_RAG_TOP_K', '5'))
    payload = _vertex_request(
        f'{get_rag_base_url()}:retrieveContexts',
        method='POST',
        payload={
            'vertexRagStore': {
                'ragResources': [{'ragCorpus': rag_corpus}],
                'similarityTopK': top_k,
            },
            'query': {'text': query},
        },
    )

    items = []
    for index, context in enumerate(payload.get('contexts', {}).get('contexts', []), start=1):
        if not isinstance(context, dict):
            continue
        items.append(
            {
                'index': index,
                'sourceUri': context.get('sourceUri') or context.get('source_uri'),
                'text': context.get('text', ''),
                'score': context.get('score'),
            }
        )

    return {
        'ragCorpus': rag_corpus,
        'count': len(items),
        'contexts': items,
    }


async def run_retrieve_rag_contexts_tool(raw_body: bytes) -> VapiToolWebhookResponse:
    payload = _decode_payload(raw_body)
    tool_calls = _extract_tool_calls(payload)
    results: list[VapiToolResult] = []

    for tool_call in tool_calls:
        args = tool_call.get('arguments')
        if not isinstance(args, dict):
            results.append(_error_result(tool_call['id'], 'Tool arguments must be an object.'))
            continue

        query = args.get('query')
        if not isinstance(query, str) or not query.strip():
            results.append(_error_result(tool_call['id'], 'Missing query argument.'))
            continue

        try:
            result = retrieve_rag_contexts(query)
        except RuntimeError as exc:
            results.append(_error_result(tool_call['id'], str(exc)))
            continue

        results.append(_success_result(tool_call['id'], result))

    return VapiToolWebhookResponse(results=results)
