import re
from typing import Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator

PHONE_REGEX = re.compile(r"^\+[1-9]\d{7,14}$")


class UserProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    time_zone: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not PHONE_REGEX.match(value):
            raise ValueError("Formato de teléfono inválido. Usa formato internacional como +34123456789")
        return value

    @field_validator("country")
    @classmethod
    def validate_country(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if len(value) != 2 or not value.isalpha():
            raise ValueError("El país debe ser un código ISO 3166-1 alpha-2 de dos letras")
        return value.upper()

    @field_validator("time_zone")
    @classmethod
    def validate_timezone(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        try:
            ZoneInfo(value)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("Zona horaria inválida. Usa un identificador IANA válido") from exc
        return value


class UserProfileRead(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass
