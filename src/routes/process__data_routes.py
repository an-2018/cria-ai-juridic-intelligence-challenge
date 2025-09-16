from fastapi import APIRouter, HTTPException

from src.application.dtos.input.process_data_input_dto import ProcessDataInputDTO
from src.application.dtos.output.process_data_output_dto import ProcessDataOutputDTO

router = APIRouter()

# @router.post("/extract", response_model=ProcessDataOutputDTO)
@router.post("/extract")
async def extract_process_data(request: ProcessDataInputDTO):
    """
    Extract data from pdf file provided as an url in the request body and returns a json containing the extracted data in a strutured format.
    """
    try:
        result = {
            "case_id": "0809090-86.2024.8.12.0021",
            "resume": "string",
            "timeline": [
                {
                "event_id": 0,
                "event_name": "string",
                "event_description": "string",
                "event_date": "YYYY-MM-DD",
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
        
        return result


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))