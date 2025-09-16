from pydantic import BaseModel, HttpUrl


class ProcessDataInputDTO(BaseModel):
    pdf_url: HttpUrl
    case_id: str