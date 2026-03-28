from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    private_key: str | None
    default_phone_number: str | None
    default_phone_number_id: str | None
    base_url: str = 'https://api.vapi.ai'


def to_camel(field_name: str) -> str:
    parts = field_name.split('_')
    return parts[0] + ''.join(part.capitalize() for part in parts[1:])


class OutboundCallRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    assistant_id: str
    customer_number: str
    phone_number_id: str | None = None
    customer_name: str | None = None


class PhoneNumbersResponse(BaseModel):
    items: list[dict[str, Any]]
