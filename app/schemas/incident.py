from datetime import datetime, timezone
from enum import StrEnum, auto
from uuid import uuid4

from typing_extensions import Self
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, model_validator, StringConstraints


class SeverityEnum(StrEnum):
    SEV1 = auto()
    SEV2 = auto()
    SEV3 = auto()
    SEV4 = auto()


class StatusEnum(StrEnum):
    OPEN = auto()
    INVESTIGATING = auto()
    MITIGATED = auto()
    RESOLVED = auto()


class IncidentCreate(BaseModel):
    title: Annotated[str,StringConstraints(max_length=200)]
    description: str
    service: str
    severity: SeverityEnum

    @field_validator('title', mode='before')
    @classmethod
    def strip(cls,value:str) -> str:
        return value.strip()


class Incident(IncidentCreate):
    id: str = uuid4()
    status: StatusEnum = StatusEnum.OPEN
    created_at: datetime=datetime.now(timezone.utc) 
    updated_at: datetime=datetime.now(timezone.utc)

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.updated_at < self.created_at:
            raise ValueError('Created date cannot be higher that updated date')


if __name__ == "__main__":
    newincident=Incident(created_at=datetime.now(),updated_at=datetime.now(),title='title1     ',description='some description',service='service1',severity=SeverityEnum.SEV1)
    print(newincident.json())
