from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field


class Settings(BaseModel):
    private_key: str | None
    assistant_id: str | None
    default_phone_number: str | None
    default_phone_number_id: str | None
    base_url: str = 'https://api.vapi.ai'

class OutboundCallRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    assistant_id: Annotated[str | None, Field(alias='assistantId')] = None
    customer_number: Annotated[str, Field(alias='customerNumber')]
    phone_number_id: Annotated[str | None, Field(alias='phoneNumberId')] = None
    customer_name: Annotated[str | None, Field(alias='customerName')] = None


class PhoneNumbersResponse(BaseModel):
    items: list[dict[str, Any]]
