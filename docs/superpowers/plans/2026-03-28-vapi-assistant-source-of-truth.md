# Vapi Assistant Source of Truth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the custom Vapi HTTP wrapper with the official Python Server SDK and make one assistant config live in repo as the source of truth.

**Architecture:** Keep the existing FastAPI routes stable, move Vapi integration behind a thin adapter over the official SDK, and add a CLI sync script that can pull and push the assistant spec. Store the assistant definition as JSON in `config/vapi/assistant.json` and target one fixed `VAPI_ASSISTANT_ID`.

**Tech Stack:** FastAPI, pydantic, pytest, Vapi Python Server SDK (`vapi_server_sdk`)

---

### Task 1: Refactor the Vapi service layer to the official SDK

**Files:**
- Modify: `api/service_vapi.py`
- Modify: `api/schemas_vapi.py`
- Modify: `api/requirements.txt`
- Test: `api/tests/test_main.py`

- [ ] **Step 1: Write the failing tests for SDK-backed behavior**

```python
def test_get_vapi_assistant() -> None:
    app.dependency_overrides = {get_vapi_client: lambda: StubVapiClient()}
    client = TestClient(app)

    response = client.get("/vapi/assistant/assistant-123")

    assert response.status_code == 200
```

```python
def test_create_call_uses_env_default_phone_number() -> None:
    stub = StubVapiClient()
    app.dependency_overrides = {
        get_settings: lambda: Settings(
            private_key="test-key",
            assistant_id="assistant-123",
            default_phone_number="+12604002243",
        ),
        get_vapi_client: lambda: stub,
    }
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_main.py -q`
Expected: FAIL because `Settings` and `VapiClient` do not yet expose the new SDK-backed contract.

- [ ] **Step 3: Write minimal implementation**

```python
from vapi import AsyncVapi
from vapi.core.api_error import ApiError


class VapiClient:
    def __init__(self, settings: Settings) -> None:
        self.client = AsyncVapi(token=settings.private_key)
```

```python
async def get_assistant(self, assistant_id: str) -> dict[str, Any]:
    assistant = await self.client.assistants.get(assistant_id)
    return assistant.model_dump(mode="json", exclude_none=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_main.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add api/service_vapi.py api/schemas_vapi.py api/requirements.txt api/tests/test_main.py
git commit -m "refactor: use Vapi server SDK in backend"
```

### Task 2: Add assistant source-of-truth config and sync CLI

**Files:**
- Create: `config/vapi/assistant.json`
- Create: `api/scripts/sync_vapi_assistant.py`
- Modify: `.env.example`
- Test: `api/tests/test_vapi_sync.py`

- [ ] **Step 1: Write the failing tests for pull and push**

```python
def test_pull_writes_assistant_json(tmp_path: Path) -> None:
    client = StubVapiClient()
    pull_assistant_config(client=client, assistant_id="assistant-123", output_path=tmp_path / "assistant.json")
    assert json.loads((tmp_path / "assistant.json").read_text())["id"] == "assistant-123"
```

```python
def test_push_updates_assistant_from_json(tmp_path: Path) -> None:
    client = StubVapiClient()
    config_path = tmp_path / "assistant.json"
    config_path.write_text(json.dumps({"name": "Mike Clone"}))
    push_assistant_config(client=client, assistant_id="assistant-123", input_path=config_path)
    assert client.updated_assistant_id == "assistant-123"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_vapi_sync.py -q`
Expected: FAIL because sync script and helpers do not exist yet.

- [ ] **Step 3: Write minimal implementation**

```python
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["pull", "push"])
```

```python
if args.command == "pull":
    assistant = asyncio.run(vapi_client.get_assistant(settings.assistant_id))
    output_path.write_text(json.dumps(assistant, indent=2) + "\n")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_vapi_sync.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add config/vapi/assistant.json api/scripts/sync_vapi_assistant.py .env.example api/tests/test_vapi_sync.py
git commit -m "feat: add Vapi assistant sync workflow"
```

### Task 3: Wire the fixed assistant ID and document the workflow

**Files:**
- Modify: `api/routes_vapi.py`
- Modify: `README.md`
- Test: `api/tests/test_main.py`

- [ ] **Step 1: Write the failing test for env-driven assistant identity**

```python
def test_default_assistant_id_can_come_from_env() -> None:
    settings = Settings(private_key="test-key", assistant_id="assistant-123")
    assert settings.assistant_id == "assistant-123"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_main.py -q`
Expected: FAIL because `assistant_id` is not yet part of settings and docs do not describe the workflow.

- [ ] **Step 3: Write minimal implementation**

```python
class Settings(BaseModel):
    private_key: str | None
    assistant_id: str | None
```

```md
VAPI_ASSISTANT_ID=f1941929-8416-486f-ba81-154de28fb7d1
python api/scripts/sync_vapi_assistant.py pull
python api/scripts/sync_vapi_assistant.py push
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_main.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add api/routes_vapi.py README.md api/tests/test_main.py
git commit -m "docs: describe Vapi assistant source-of-truth flow"
```
