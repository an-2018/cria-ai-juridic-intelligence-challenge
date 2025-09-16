import datetime

from pydantic import BaseModel

"""
Output DTO Example:
{
  "case_id": "0809090-86.2024.8.12.0021",
  "resume": "string",
  "timeline": [
    {
      "event_id": 0,
      "event_name": "string",
      "event_description": "string",
      "event_date": "2024-08-28",
      "event_page_init": 1,
      "event_page_end": 2
    }
  ],
  "evidence": [
    {
      "evidence_id": 0,
      "evidence_name": "string",
      "evidence_flaw": "string | null",
      "evidence_page_init": 10,
      "evidence_page_end": 12
    }
  ],
  "persisted_at": "2025-08-28T00:00:00Z"
}
"""

class TimelineEventDTO(BaseModel):
    event_id: int
    event_name: str
    event_description: str
    event_date: datetime.date
    event_page_init: int
    event_page_end: int

class EvidenceDTO(BaseModel):
    evidence_id: int
    evidence_name: str
    evidence_flaw: str | None
    evidence_page_init: int
    evidence_page_end: int

class ProcessDataOutputDTO(BaseModel):
    case_id: str
    resume: str
    timeline: list[TimelineEventDTO]
    evidence: list[EvidenceDTO]
    persisted_at: datetime.datetime
