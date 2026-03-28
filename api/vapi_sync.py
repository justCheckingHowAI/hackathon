from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, Protocol


SERVER_GENERATED_ASSISTANT_FIELDS = {
    'id',
    'orgId',
    'createdAt',
    'updatedAt',
    'isServerUrlSecretSet',
}


class AssistantSyncClient(Protocol):
    async def get_assistant(self, assistant_id: str) -> dict[str, Any]: ...

    async def update_assistant(self, assistant_id: str, payload: dict[str, Any]) -> dict[str, Any]: ...


def normalize_assistant_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in payload.items()
        if key not in SERVER_GENERATED_ASSISTANT_FIELDS and value is not None
    }


def pull_assistant_config(
    *,
    client: AssistantSyncClient,
    assistant_id: str,
    output_path: Path,
) -> dict[str, Any]:
    payload = asyncio.run(client.get_assistant(assistant_id))
    normalized = normalize_assistant_payload(payload)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(normalized, indent=2) + '\n')
    return normalized


def push_assistant_config(
    *,
    client: AssistantSyncClient,
    assistant_id: str,
    input_path: Path,
) -> dict[str, Any]:
    payload = json.loads(input_path.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f'Assistant config must be a JSON object: {input_path}')
    return asyncio.run(client.update_assistant(assistant_id, payload))
