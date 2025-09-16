import logging
from datetime import datetime, timezone
from src.application.dtos.input.process_data_input_dto import ProcessDataInputDTO
from src.application.dtos.output.process_data_output_dto import ProcessDataOutputDTO
from src.application.services.process_data_service import ProcessDataService

class ProcessDataUseCase:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.process_data_service = ProcessDataService()

    def execute(self, input_dto: ProcessDataInputDTO) -> ProcessDataOutputDTO:
        self.logger.info(f"Executing ProcessDataUseCase with input: {input_dto}")
        # download PDF from url
        pdf_binary =self.process_data_service.dowload_pdf_from_url(input_dto.pdf_url.encoded_string())
        
        # extract infromation from pdf binary
        pdf_data = self.process_data_service.extract_information_from_pdf(pdf_binary)
        
        # map and validate data with ProcessDataOutputDTO
        output_dto = ProcessDataOutputDTO(**{
                "case_id": input_dto.case_id,
                "persisted_at": datetime.now(timezone.utc),
                **pdf_data
            })
        
        # persist extracted data in database
        
        # return ProcessDataOutputDTO
        return output_dto