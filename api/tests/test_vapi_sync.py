import json
from pathlib import Path

from vapi_sync import normalize_assistant_payload, pull_assistant_config, push_assistant_config


class StubVapiSyncClient:
    def __init__(self) -> None:
        self.updated_assistant_id: str | None = None
        self.updated_payload: dict | None = None

    async def get_assistant(self, assistant_id: str) -> dict:
        return {
            "id": assistant_id,
            "orgId": "org-123",
            "createdAt": "2026-03-28T10:00:00Z",
            "updatedAt": "2026-03-28T10:05:00Z",
            "name": "Mike Clone",
            "firstMessage": "Hello",
            "model": {"provider": "openai", "model": "gpt-4o-mini"},
            "voice": {"provider": "11labs", "voiceId": "abc"},
        }

    async def update_assistant(self, assistant_id: str, payload: dict) -> dict:
        self.updated_assistant_id = assistant_id
        self.updated_payload = payload
        return {"id": assistant_id, **payload}


def test_normalize_assistant_payload_removes_server_generated_fields() -> None:
    normalized = normalize_assistant_payload(
        {
            "id": "assistant-123",
            "orgId": "org-123",
            "createdAt": "2026-03-28T10:00:00Z",
            "updatedAt": "2026-03-28T10:05:00Z",
            "name": "Mike Clone",
            "model": {"provider": "openai", "model": "gpt-4o-mini"},
        }
    )

    assert normalized == {
        "name": "Mike Clone",
        "model": {"provider": "openai", "model": "gpt-4o-mini"},
    }


def test_pull_assistant_config_writes_normalized_json(tmp_path: Path) -> None:
    client = StubVapiSyncClient()
    output_path = tmp_path / "assistant.json"

    pull_assistant_config(client=client, assistant_id="assistant-123", output_path=output_path)

    assert json.loads(output_path.read_text()) == {
        "name": "Mike Clone",
        "firstMessage": "Hello",
        "model": {"provider": "openai", "model": "gpt-4o-mini"},
        "voice": {"provider": "11labs", "voiceId": "abc"},
    }


def test_push_assistant_config_updates_existing_assistant(tmp_path: Path) -> None:
    client = StubVapiSyncClient()
    input_path = tmp_path / "assistant.json"
    input_path.write_text(
        json.dumps(
            {
                "name": "Repo Assistant",
                "model": {"provider": "openai", "model": "gpt-4o"},
            }
        )
    )

    push_assistant_config(client=client, assistant_id="assistant-123", input_path=input_path)

    assert client.updated_assistant_id == "assistant-123"
    assert client.updated_payload == {
        "name": "Repo Assistant",
        "model": {"provider": "openai", "model": "gpt-4o"},
    }
