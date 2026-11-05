from datetime import UTC, datetime
from enum import StrEnum, auto
from typing import Annotated, Self
from uuid import UUID, uuid4

from pydantic import (
    AwareDatetime,
    BaseModel,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)


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
    title: Annotated[str,StringConstraints(min_length=1, max_length=200)]
    description: str
    service: str
    severity: SeverityEnum

    @field_validator('title', mode='before')
    @classmethod
    def strip(cls,value:str) -> str:
        return value.strip()


class Incident(IncidentCreate):
    id: UUID = Field(default_factory=lambda: uuid4(), validate_default=True)
    
    status: StatusEnum = StatusEnum.OPEN
    created_at: AwareDatetime = Field(default_factory=lambda: datetime.now(UTC), validate_default=True)
    updated_at: AwareDatetime = Field(default_factory=lambda: datetime.now(UTC), validate_default=True)

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.created_at > self.updated_at:
            raise ValueError('Created date cannot be later than updated date')
        return self

if __name__ == "__main__":
    newincident=Incident(title='title1     ',description='some description',service='service1',severity=SeverityEnum.SEV1)
    newincident2=Incident(title='title1     ',description='some description',service='service1',severity=SeverityEnum.SEV1)
    print(newincident.model_dump_json())
    print(newincident2.model_dump_json())
