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

class ServiceEnum(StrEnum):
    SERV1 = "service 1"
    SERV2 = "service 2"
    SERV3 = "service 3"
    SERV4 = "service 4"


class IncidentCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    title: Annotated[str,StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
    description: str
    service: ServiceEnum
    severity: SeverityEnum

class Incident(IncidentCreate):
    id: UUID = Field(default_factory=lambda: uuid4(), validate_default=True)
    
    status: StatusEnum = StatusEnum.OPEN
    created_at: AwareDatetime
    updated_at: AwareDatetime

    @model_validator(mode='before')
    def set_default_timestamps(self) -> Self:
        current_timestamp=datetime.now(UTC)
        if "created_at" not in self:
            self["created_at"] = current_timestamp
        if "updated_at" not in self:
             self["updated_at"] = current_timestamp
        return self

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.created_at > self.updated_at:
            raise ValueError('Created date cannot be later than updated date')
        return self


if __name__ == "__main__":
    newincident=Incident(title='     ',description='some description', service=serviceEnum.SERV1,severity=SeverityEnum.SEV1)
    newincident2=Incident(title='title1     ',description='some description', service=serviceEnum.SERV2,severity=SeverityEnum.SEV1)
    print(newincident.model_dump_json())
    print(newincident2.model_dump_json())
