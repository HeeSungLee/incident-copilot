from enum import StrEnum, auto
from pydantic import BaseModel
from datetime import datetime

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
    title: str
    description: str
    service: str
    severity: SeverityEnum = SeverityEnum.SEV4


class Incident(BaseModel):
    id
    title: str
    description: str
    service: str
    severity: SeverityEnum = SeverityEnum.SEV4
    status: StatusEnum = StatusEnum.OPEN
    created_at: datetime
    updated_at: datetime