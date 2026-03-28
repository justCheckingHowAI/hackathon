import json

from fastapi.testclient import TestClient

from hiring_packs_store import HiringPacksStore
from main import Settings, app, get_settings, get_vapi_client
from tools import GENERATE_HIRING_PACK_RESULT, WHOAMI_RESULT


class StubVapiClient:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    async def get_assistant(self, assistant_id: str) -> dict:
        return {
            "id": assistant_id,
            "name": "Mike Clone",
            "model": {"provider": "openai", "model": "gpt-4o-mini"},
        }

    async def list_phone_numbers(self) -> list[dict]:
        return [
            {"id": "phone-1", "number": "+12604002243", "provider": "twilio"},
            {"id": "phone-2", "number": "+15551234567", "provider": "twilio"},
        ]

    async def create_call(self, payload: dict) -> dict:
        self.calls.append(payload)
        return {
            "id": "call-123",
            "status": "queued",
            "assistantId": payload["assistantId"],
            "phoneNumberId": payload["phoneNumberId"],
            "customer": payload["customer"],
        }


def setup_function() -> None:
    app.dependency_overrides = {}


def test_get_vapi_assistant() -> None:
    app.dependency_overrides = {get_vapi_client: lambda: StubVapiClient()}
    client = TestClient(app)

    response = client.get("/vapi/assistant/assistant-123")

    assert response.status_code == 200
    assert response.json() == {
        "id": "assistant-123",
        "name": "Mike Clone",
        "model": {"provider": "openai", "model": "gpt-4o-mini"},
    }


def test_list_vapi_phone_numbers() -> None:
    app.dependency_overrides = {get_vapi_client: lambda: StubVapiClient()}
    client = TestClient(app)

    response = client.get("/vapi/phone-numbers")

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {"id": "phone-1", "number": "+12604002243", "provider": "twilio"},
            {"id": "phone-2", "number": "+15551234567", "provider": "twilio"},
        ]
    }


def test_create_call_uses_env_default_phone_number() -> None:
    stub = StubVapiClient()
    app.dependency_overrides = {
        get_settings: lambda: Settings(
            private_key="test-key",
            assistant_id="assistant-from-env",
            default_phone_number_id=None,
            default_phone_number="+12604002243",
            base_url="https://api.vapi.ai",
        ),
        get_vapi_client: lambda: stub,
    }
    client = TestClient(app)

    response = client.post(
        "/vapi/calls",
        json={
            "customerNumber": "+48123123123",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": "call-123",
        "status": "queued",
        "assistantId": "assistant-from-env",
        "phoneNumberId": "phone-1",
        "customer": {"number": "+48123123123"},
    }
    assert stub.calls == [
        {
            "assistantId": "assistant-from-env",
            "phoneNumberId": "phone-1",
            "customer": {"number": "+48123123123"},
        }
    ]


def test_create_call_accepts_explicit_phone_number_id() -> None:
    stub = StubVapiClient()
    app.dependency_overrides = {
        get_settings: lambda: Settings(
            private_key="test-key",
            assistant_id="assistant-from-env",
            default_phone_number_id=None,
            default_phone_number=None,
            base_url="https://api.vapi.ai",
        ),
        get_vapi_client: lambda: stub,
    }
    client = TestClient(app)

    response = client.post(
        "/vapi/calls",
        json={
            "assistantId": "assistant-123",
            "customerNumber": "+48123123123",
            "phoneNumberId": "phone-2",
            "customerName": "Maks",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": "call-123",
        "status": "queued",
        "assistantId": "assistant-123",
        "phoneNumberId": "phone-2",
        "customer": {"number": "+48123123123", "name": "Maks"},
    }


def test_create_call_accepts_explicit_assistant_id() -> None:
    stub = StubVapiClient()
    app.dependency_overrides = {
        get_settings: lambda: Settings(
            private_key="test-key",
            assistant_id="assistant-from-env",
            default_phone_number_id="phone-2",
            default_phone_number=None,
            base_url="https://api.vapi.ai",
        ),
        get_vapi_client: lambda: stub,
    }
    client = TestClient(app)

    response = client.post(
        "/vapi/calls",
        json={
            "assistantId": "assistant-explicit",
            "customerNumber": "+48123123123",
        },
    )

    assert response.status_code == 200
    assert response.json()["assistantId"] == "assistant-explicit"


def test_create_call_requires_phone_number_config() -> None:
    app.dependency_overrides = {
        get_settings: lambda: Settings(
            private_key="test-key",
            assistant_id="assistant-from-env",
            default_phone_number_id=None,
            default_phone_number=None,
            base_url="https://api.vapi.ai",
        ),
        get_vapi_client: lambda: StubVapiClient(),
    }
    client = TestClient(app)

    response = client.post(
        "/vapi/calls",
        json={
            "assistantId": "assistant-123",
            "customerNumber": "+48123123123",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "phoneNumberId is required or configure "
            "VAPI_DEFAULT_PHONE_NUMBER_ID / VAPI_DEFAULT_PHONE_NUMBER."
        )
    }


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
                "result": WHOAMI_RESULT,
            }
        ]
    }


def test_whoami_tool_ignores_tool_name_on_dedicated_endpoint() -> None:
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
                "result": WHOAMI_RESULT,
            }
        ]
    }


def test_generate_hiring_pack_tool_saves_demo_pack(monkeypatch, tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    demo_payload = {
        "person": {
            "id": "mike",
            "name": "Mike Grabowski",
            "role": "Senior React Native Engineer & OSS Lead",
            "avatar": "MG",
            "department": "Engineering",
            "yearsAtCompany": 6,
            "keyProjects": ["React Native CLI"],
        },
        "skills": [],
        "gapSummary": "demo",
        "recommendedRole": {
            "title": "Staff React Native Platform Engineer",
            "description": "demo",
            "seniority": "Staff / Principal",
        },
        "scorecard": [],
        "interviewQuestions": [],
        "mustHave": [],
        "niceToHave": [],
        "redFlags": [],
    }
    (tmp_path / "demo-hiring-pack.json").write_text(
        json.dumps(demo_payload),
        encoding="utf-8",
    )
    monkeypatch.setattr("tools.get_hiring_packs_store", lambda: store)
    client = TestClient(app)

    response = client.post(
        "/vapi/tools/generate-hiring-pack",
        json={
            "message": {
                "type": "tool-calls",
                "toolCallList": [
                    {
                        "id": "tool-call-hiring-pack-1",
                        "name": "generate_hiring_pack",
                        "arguments": {"ignored": True},
                    }
                ],
            }
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "toolCallId": "tool-call-hiring-pack-1",
                "result": GENERATE_HIRING_PACK_RESULT,
            }
        ]
    }
    assert (tmp_path / "mike.json").exists()


def test_generate_hiring_pack_tool_returns_error_when_demo_missing(monkeypatch, tmp_path) -> None:
    store = HiringPacksStore(base_dir=tmp_path)
    monkeypatch.setattr("tools.get_hiring_packs_store", lambda: store)
    client = TestClient(app)

    response = client.post(
        "/vapi/tools/generate-hiring-pack",
        json={
            "message": {
                "type": "tool-calls",
                "toolCallList": [
                    {
                        "id": "tool-call-hiring-pack-2",
                        "name": "generate_hiring_pack",
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
                "toolCallId": "tool-call-hiring-pack-2",
                "error": "Could not find demo hiring pack: demo-hiring-pack.json.",
            }
        ]
    }


def test_run_cypher_query_tool_returns_database_result(monkeypatch) -> None:
    client = TestClient(app)

    def fake_run_cypher_query(query: str, parameters: dict) -> dict:
        assert query == "MATCH (n) RETURN count(n) AS count LIMIT 1"
        assert parameters == {"label": "Person"}
        return {
            "columns": ["count"],
            "rowCount": 1,
            "rows": [[42]],
        }

    monkeypatch.setattr("tools.run_cypher_query", fake_run_cypher_query)

    response = client.post(
        "/vapi/tools/run-cypher-query",
        json={
            "message": {
                "type": "tool-calls",
                "toolCallList": [
                    {
                        "id": "tool-call-cypher-1",
                        "name": "run_cypher_query",
                        "arguments": {
                            "query": "MATCH (n) RETURN count(n) AS count LIMIT 1",
                            "parameters": {"label": "Person"},
                        },
                    }
                ],
            }
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "toolCallId": "tool-call-cypher-1",
                "result": {
                    "columns": ["count"],
                    "rowCount": 1,
                    "rows": [[42]],
                },
            }
        ]
    }


def test_run_cypher_query_tool_returns_error_for_blocked_query(monkeypatch) -> None:
    client = TestClient(app)

    def fake_run_cypher_query(query: str, parameters: dict) -> dict:
        raise ValueError("Only read-only Cypher queries are allowed.")

    monkeypatch.setattr("tools.run_cypher_query", fake_run_cypher_query)

    response = client.post(
        "/vapi/tools/run-cypher-query",
        json={
            "message": {
                "type": "tool-calls",
                "toolCallList": [
                    {
                        "id": "tool-call-cypher-2",
                        "name": "run_cypher_query",
                        "arguments": {
                            "query": "CREATE (n:Test)",
                        },
                    }
                ],
            }
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "toolCallId": "tool-call-cypher-2",
                "error": "Only read-only Cypher queries are allowed.",
            }
        ]
    }


def test_retrieve_rag_contexts_tool_returns_contexts(monkeypatch) -> None:
    client = TestClient(app)

    def fake_retrieve_rag_contexts(query: str) -> dict:
        assert query == "What is Mike working on?"
        return {
            "ragCorpus": "projects/test/locations/europe-west2/ragCorpora/123",
            "count": 1,
            "contexts": [
                {
                    "index": 1,
                    "sourceUri": "gs://docs/mike.txt",
                    "text": "Mike works on AI voice tooling.",
                    "score": 0.91,
                }
            ],
        }

    monkeypatch.setattr("tools.retrieve_rag_contexts", fake_retrieve_rag_contexts)

    response = client.post(
        "/vapi/tools/retrieve-rag-contexts",
        json={
            "message": {
                "type": "tool-calls",
                "toolCallList": [
                    {
                        "id": "tool-call-rag-1",
                        "name": "retrieve_rag_contexts",
                        "arguments": {
                            "query": "What is Mike working on?",
                        },
                    }
                ],
            }
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "toolCallId": "tool-call-rag-1",
                "result": {
                    "ragCorpus": "projects/test/locations/europe-west2/ragCorpora/123",
                    "count": 1,
                    "contexts": [
                        {
                            "index": 1,
                            "sourceUri": "gs://docs/mike.txt",
                            "text": "Mike works on AI voice tooling.",
                            "score": 0.91,
                        }
                    ],
                },
            }
        ]
    }


def test_tool_endpoint_returns_empty_results_for_invalid_payload() -> None:
    client = TestClient(app)

    response = client.post(
        "/vapi/tools/retrieve-rag-contexts",
        content=b"not-json",
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 200
    assert response.json() == {"results": []}
