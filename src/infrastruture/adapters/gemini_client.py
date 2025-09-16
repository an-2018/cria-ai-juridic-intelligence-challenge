import json
import logging
import os
from src.domain.ports.llm_client_interface import ILlmClient
from google import genai
from src.infrastruture.configs.app_config import settings

environ = __import__('os').environ

class GeminiClient(ILlmClient):
    """Implementation of the LLM client using Gemini API"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL_NAME
        self.client = genai.Client(api_key=api_key)

    def _get_extraction_prompt(self) -> str:
        """Returns the system prompt for the extration of the data into an strutured json format"""
        return """
        Your are a specialized legal assistant AI. Your task is to analyze the provided legal process document PDF
        and extract the relevant and key information into a structured JSON format. 
        
        The response must be a single valid JSON object without any additional text or explanation. Do not inlcude marckdown formatting like ```json.

        The JSON object must have three top-level keys: "resume", "timeline", and "evidence".

        1.  "resume": Provide a concise text summary of the legal case.
        2.  "timeline": Create a list of all relevant events in chronological order. Each event must be an object with these exact keys:
            - "event_id": integer, starting from 0.
            - "event_name": string, a short title for the event (e.g., "Ajuizamento da Ação", "Decisão Interlocutória").
            - "event_description": string, a detailed description of the event.
            - "event_date": string, in "YYYY-MM-DD" format.
            - "event_page_init": integer, the starting page number of the event.
            - "event_page_end": integer, the ending page number of the event.
        3.  "evidence": Create a list of all attached evidence/proofs. Each item must be an object with these exact keys:
            - "evidence_id": integer, starting from 0.
            - "evidence_name": string, the name of the document (e.g., "Fatura CredNet", "Procuração").
            - "evidence_flaw": string, describe any inconsistencies or "Sem inconsistências" if none.
            - "evidence_page_init": integer, the starting page number.
            - "evidence_page_end": integer, the ending page number.

        Ensure the JSON structure is strictly followed, with correct key names and data types. If certain information is not available, use null for strings and -1 for integers.

        Analyze the entire document carefully to ensure all events and evidence are captured accurately. The goal is to provide a clear, structured overview of the legal case based on the document content.
        """

    def extract_data_from_pdf(self, file_path: str) -> dict:
        """Uses the Gemini API to extract the information from the PDF binary and returns it as a dictionary"""
        try:
            # pdf_file = self.client.files.upload(
            #     file=pdf_binary,
            #     config={"file_type": "application/pdf", "name": "legal_process.pdf"}
            # )
            pdf_file = self.client.files.upload(
                file=file_path,
                config={
                    "mime_type": "application/pdf",
                    "display_name": "legal_process.pdf"
                }
            )


            prompt = self._get_extraction_prompt()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    prompt,
                    pdf_file,
                    "Extract the data from the legal process document into the required JSON format."
                ],
                config={"response_mime_type": "application/json"}
            )

            self.logger.info(f"Gemini API response: {response}")
            content = getattr(response, "text", None)

            if not content:
                response_dict = response.model_dump_json()
                response_dict = json.loads(response_dict)
                content = response_dict.get("text", "")
                if not content:
                    raise ValueError("No text content found in Gemini API response")

            # Attempt to parse the content as JSON
            try:
                json_data = json.loads(content)
                return json_data
            except json.JSONDecodeError as json_err:
                self.logger.error(f"JSON decoding error: {json_err}")
                self.logger.error(f"Response content: {content}")
                raise ValueError("Failed to parse JSON from Gemini API response")

        except Exception as e:
            self.logger.error(f"Error extracting data from PDF: {e}")
            raise e
        
        finally:
            if file_path:
                try:
                    os.remove(file_path)
                    self.logger.info(f"Temporary file {file_path} removed successfully.")
                except Exception as cleanup_err:
                    self.logger.warning(f"Failed to remove temporary file {file_path}: {cleanup_err}")