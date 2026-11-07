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
    ConfigDict
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

class serviceEnum(StrEnum):
    SERV1 = "service 1"
    SERV2 = "service 2"
    SERV3 = "service 3"
    SERV4 = "service 4"


class IncidentCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    title: Annotated[str,StringConstraints(min_length=1, max_length=200)]
    description: str
    service: serviceEnum
    severity: SeverityEnum

    @field_validator('title', mode='after')
    @classmethod
    def strip(cls,value:str) -> str:
        stripped_str=value.strip()
        if stripped_str=="":
            raise ValueError('The title should be between 1 and 200 characters')
        return stripped_str


class Incident(IncidentCreate):
    id: UUID = Field(default_factory=lambda: uuid4(), validate_default=True)
    
    status: StatusEnum = StatusEnum.OPEN
    created_at: AwareDatetime | None = None
    updated_at: AwareDatetime | None = None

    @model_validator(mode='after')
    def set_default_timestamps(self) -> Self:
        current_timestamp=datetime.now(UTC)
        if self.created_at is None:
            self.created_at = current_timestamp
        if self.updated_at is None:
            self.updated_at = current_timestamp
        return self

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.created_at > self.updated_at:
            raise ValueError('Created date cannot be later than updated date')
        return self


if __name__ == "__main__":
    newincident=Incident(title='title1     ',description='some description', service=serviceEnum.SERV1,severity=SeverityEnum.SEV1)
    newincident2=Incident(title='title1     ',description='some description', service=serviceEnum.SERV2,severity=SeverityEnum.SEV1)
    print(newincident.model_dump_json())
    print(newincident2.model_dump_json())
