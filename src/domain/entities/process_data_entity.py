import datetime
from typing import List
from pydantic import BaseModel, Field

class TimelineEvent(BaseModel):
    event_id: int = Field(..., description="Unique identifier for the event")
    event_name: str = Field(..., description="Name of the event")
    event_description: str = Field(..., description="Detailed description of the event")
    event_date: datetime.date = Field(..., description="Date when the event occurred")
    event_page_init: int = Field(..., description="Starting page number of the event in the document")
    event_page_end: int = Field(..., description="Ending page number of the event in the document")

class Evidence(BaseModel):
    evidence_id: int = Field(..., description="Unique identifier for the evidence")
    evidence_name: str = Field(..., description="Name of the evidence")
    evidence_flaw: str | None = Field(None, description="Description of any flaws in the evidence, if applicable")
    evidence_page_init: int = Field(..., description="Starting page number of the evidence in the document")
    evidence_page_end: int = Field(..., description="Ending page number of the evidence in the document")

class ProcessDataEntity(BaseModel):
    case_id: str = Field(..., description="Unique identifier for the legal case")
    resume: str = Field(..., description="Summary of the legal case")
    timeline: list[TimelineEvent] = Field(..., description="List of significant events in the case timeline")
    evidence: list[Evidence] = Field(..., description="List of evidence items related to the case")
    persisted_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), description="Timestamp when the data was persisted")