from pydantic import BaseModel, HttpUrl, Field


class ProcessDataInputDTO(BaseModel):
    pdf_url: HttpUrl
    case_id: str = Field(..., example="0809090-86.2024.8.12.0021")