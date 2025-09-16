import requests
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
class ProcessDataService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    
    def dowload_pdf_from_url(self, url: str) -> bytes:
        try:
            self.logger.info(f"Downloading PDF from URL: {url}")

            # Validate URL format
            parsed_url = urlparse(url)
            if not parsed_url.path.lower().endswith('.pdf'):
                self.logger.warning(f"URL is not a direct link to a PDF")

            response = requests.get(url)
            response.raise_for_status()

            # Validate Content-Type header
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/pdf" not in content_type:
                raise ValueError(f"Expected content type 'application/pdf' but got '{content_type}'")

            pdf_content = response.content

            # Validate file signature for PDF
            if not pdf_content.startswith(b'%PDF-'):
                raise ValueError("Downloaded file is not a valid PDF.")

            self.logger.info(f"Successfully downloaded and validated PDF from URL")
            return pdf_content
        except Exception as e:
            self.logger.error(f"Failed to download or validate PDF from URL: {e}", exc_info=True)
            raise Exception(f"Failed to process PDF from URL: {e}") from e
    
    def extract_information_from_pdf(self, pdf_binary: bytes) -> dict:

        return {
            "case_id": "0809090-86.2024.8.12.0021",
            "resume": "string",
            "timeline": [
                {
                "event_id": 0,
                "event_name": "string",
                "event_description": "string",
                "event_date": "2025-09-16",
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