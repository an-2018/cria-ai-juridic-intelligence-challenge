from fastapi import APIRouter, Depends, HTTPException

from src.application.dtos.input.process_data_input_dto import ProcessDataInputDTO
from src.application.dtos.output.process_data_output_dto import ProcessDataOutputDTO
from src.application.use_cases.extract_process_data_use_case import ProcessDataUseCase

router = APIRouter()

# @router.post("/extract", response_model=ProcessDataOutputDTO)
@router.post("/extract")
async def extract_process_data(request: ProcessDataInputDTO, process_data_use_case: ProcessDataUseCase = Depends(ProcessDataUseCase)):
    """
    Extract data from pdf file provided as an url in the request body and returns a json containing the extracted data in a strutured format.
    """
    try:
        result = process_data_use_case.execute(request)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))