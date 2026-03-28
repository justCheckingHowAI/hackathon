from fastapi.testclient import TestClient

from main import Settings, app, get_settings, get_vapi_client


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
