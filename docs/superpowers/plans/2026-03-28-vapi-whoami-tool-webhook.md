# Vapi WhoAmI Tool Webhook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `whoami` custom Vapi tool backed by a FastAPI webhook, wire it into `config/vapi/assistant.json`, and document a local `localtunnel` testing flow.

**Architecture:** Keep the first tool intentionally simple. The assistant config will define a single `model.tools` function with a tool-specific `server.url`, while FastAPI exposes one dedicated webhook endpoint that accepts Vapi tool-calls and returns a static Mike Grabowski identity result. Tests will drive the webhook contract before implementation code is added.

**Tech Stack:** FastAPI, Pydantic, pytest, Vapi assistant JSON config

---

### Task 1: Add webhook contract tests first

**Files:**
- Modify: `api/tests/test_main.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_whoami_tool_returns_result() -> None:
    client = TestClient(app)

    response = client.post(
        "/vapi/tools/whoami",
        json={
            "message": {
                "type": "tool-calls",
                "toolCallList": [
                    {
                        "id": "tool-call-123",
                        "name": "whoami",
                        "arguments": {},
                    }
                ],
            }
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "toolCallId": "tool-call-123",
                "result": (
                    "You are Mike Grabowski, CTO & Founder at Callstack. "
                    "Public profile: https://www.callstack.com/team/mike-grabowski"
                ),
            }
        ]
    }


def test_whoami_tool_rejects_unsupported_tool_name() -> None:
    client = TestClient(app)

    response = client.post(
        "/vapi/tools/whoami",
        json={
            "message": {
                "type": "tool-calls",
                "toolCallList": [
                    {
                        "id": "tool-call-999",
                        "name": "not-whoami",
                        "arguments": {},
                    }
                ],
            }
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "toolCallId": "tool-call-999",
                "error": "Unsupported tool call for this endpoint: not-whoami",
            }
        ]
    }
```

- [ ] **Step 2: Run the focused tests to verify RED**

Run: `python3 -m pytest api/tests/test_main.py -k whoami -q`
Expected: FAIL with `404` or missing route behavior because `/vapi/tools/whoami` does not exist yet.

- [ ] **Step 3: Commit the red test**

```bash
git add api/tests/test_main.py
git commit -m "test: cover Vapi whoami tool webhook"
```

### Task 2: Implement the minimal webhook handler

**Files:**
- Modify: `api/schemas_vapi.py`
- Modify: `api/routes_vapi.py`

- [ ] **Step 1: Add request and response schemas**

```python
class VapiToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class VapiToolCallsMessage(BaseModel):
    type: str
    tool_call_list: Annotated[list[VapiToolCall], Field(alias="toolCallList")] = Field(
        default_factory=list
    )


class VapiToolWebhookRequest(BaseModel):
    message: VapiToolCallsMessage


class VapiToolResult(BaseModel):
    tool_call_id: Annotated[str, Field(alias="toolCallId")]
    result: str | None = None
    error: str | None = None


class VapiToolWebhookResponse(BaseModel):
    results: list[VapiToolResult]
```

- [ ] **Step 2: Add the minimal route implementation**

```python
WHOAMI_RESULT = (
    "You are Mike Grabowski, CTO & Founder at Callstack. "
    "Public profile: https://www.callstack.com/team/mike-grabowski"
)


@router.post('/vapi/tools/whoami')
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
```

- [ ] **Step 3: Run the focused tests to verify GREEN**

Run: `python3 -m pytest api/tests/test_main.py -k whoami -q`
Expected: PASS

- [ ] **Step 4: Commit the webhook implementation**

```bash
git add api/schemas_vapi.py api/routes_vapi.py
git commit -m "feat: add Vapi whoami tool webhook"
```

### Task 3: Wire assistant config and docs

**Files:**
- Modify: `config/vapi/assistant.json`
- Modify: `README.md`
- Modify: `api/tests/test_main.py`

- [ ] **Step 1: Add assistant config for `model.tools` and prompt instructions**

```json
{
  "model": {
    "messages": [
      {
        "role": "system",
        "content": "When the caller asks who you are, whose clone you are, or who you represent, use the whoami tool before answering."
      }
    ],
    "tools": [
      {
        "type": "function",
        "name": "whoami",
        "description": "Returns the identity of the person this assistant is cloning.",
        "parameters": {
          "type": "object",
          "properties": {},
          "required": []
        },
        "server": {
          "url": "https://api.gemellus.app/vapi/tools/whoami"
        }
      }
    ]
  }
}
```

- [ ] **Step 2: Document local testing with `localtunnel`**

```md
## Vapi tool webhook testing

1. Start the API locally.
2. Expose it with localtunnel:
   `lt --port 8001`
3. Replace the `whoami` tool `server.url` in `config/vapi/assistant.json` with the localtunnel URL.
4. Push the assistant config:
   `PYTHONPATH=api python3 api/scripts/sync_vapi_assistant.py push`
5. Ask the assistant who it is cloning and confirm the `whoami` tool is invoked.
```

- [ ] **Step 3: Run the relevant tests**

Run: `python3 -m pytest api/tests/test_main.py -q`
Expected: PASS

- [ ] **Step 4: Commit config and docs**

```bash
git add config/vapi/assistant.json README.md api/tests/test_main.py
git commit -m "docs: wire Vapi whoami tool config and testing flow"
```
