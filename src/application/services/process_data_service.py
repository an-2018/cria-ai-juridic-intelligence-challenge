import tempfile
import requests
import logging
from urllib.parse import urlparse
from src.infrastruture.adapters.gemini_client import GeminiClient

logger = logging.getLogger(__name__)
class ProcessDataService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.llm_client =  GeminiClient()
        
    
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
        """
        Extracts structured data from a PDF file binary using the GeminiClient.

        Args:
            pdf_binary: the pdf file in binary format.

        Returns:
            a dictionary with the information extracted from the pdf document ('resume', 'timeline', 'evidence').
        """
        """
        try:
            self.logger.info("Extracting information from PDF using GeminiClient")

            # save binary to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(pdf_binary)
                temp_pdf_path = temp_pdf.name
                self.logger.info(f"Temporary PDF file created at: {temp_pdf_path}")

            extracted_data = self.llm_client.extract_data_from_pdf(temp_pdf_path)
            self.logger.info("Successfully extracted information from PDF")

            return extracted_data
        except Exception as e:
            self.logger.error(f"Failed to extract information from PDF: {e}", exc_info=True)
            raise Exception(f"Failed to extract information from PDF: {e}") from e
        """
        # Mocked response for demonstration purposes
        return {
            "resume": "This is a legal case involving José Ribamar Alves Filho, who is suing Fundo de Investimento em Direitos Creditorios Nao Padronizados NPL II for alleged inexistência de débitos and damages.",
            "timeline": [
                {
                "event_id": 0,
                "event_name": "Ajuizamento da Ação",
                "event_description": "José Ribamar Alves Filho proposes an \"Ação Declaratória de Inexistência de Débitos c/c Indenização por Danos Morais e Pedido de Antecipação dos Efeitos da Tutela Provisória de Urgência\" against FUNDO DE INVESTIMENTO EM DIREITOS CREDITÓRIOS NAO PADRONIZADOS NPL II.",
                "event_date": "2024-10-22",
                "event_page_init": 1,
                "event_page_end": 1
                },
                {
                "event_id": 1,
                "event_name": "Designação de Audiência",
                "event_description": "Audiência de Conciliação designada para o dia 24/03/2025 às 14:20.",
                "event_date": "2024-11-27",
                "event_page_init": 37,
                "event_page_end": 37
                },
                {
                "event_id": 2,
                "event_name": "Remessa de Relação",
                "event_description": "Certidão de Remessa de Relação referente a decisão que defere tutela.",
                "event_date": "2024-11-14",
                "event_page_init": 35,
                "event_page_end": 35
                },
                {
                "event_id": 3,
                "event_name": "Publicação da Relação",
                "event_description": "Publicação da Relação referente a decisão que defere tutela.",
                "event_date": "2024-11-18",
                "event_page_init": 36,
                "event_page_end": 36
                },
                {
                "event_id": 4,
                "event_name": "Carta de Citação e Intimação",
                "event_description": "Expedição de Carta de Citação e Intimação para audiência de conciliação.",
                "event_date": "2025-01-07",
                "event_page_init": 131,
                "event_page_end": 131
                },
                {
                "event_id": 5,
                "event_name": "Ata de Audiência",
                "event_description": "Realizada audiência de conciliação, sem acordo.",
                "event_date": "2025-03-24",
                "event_page_init": 139,
                "event_page_end": 139
                },
                {
                "event_id": 6,
                "event_name": "Juntada de Documentos",
                "event_description": "A parte Ré apresenta documentos.",
                "event_date": "2025-03-21",
                "event_page_init": 40,
                "event_page_end": 40
                },
                {
                "event_id": 7,
                "event_name": "Substabelecimento",
                "event_description": "Substabelecimento de poderes.",
                "event_date": "2025-03-21",
                "event_page_init": 135,
                "event_page_end": 135
                }
            ],
            "evidence": [
                { "evidence_id": 0, "evidence_name": "Documentos anexos", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 1, "evidence_page_end": 1 },
                { "evidence_id": 1, "evidence_name": "Comprovante de mácula", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 2, "evidence_page_end": 2 },
                { "evidence_id": 2, "evidence_name": "CredNet Light", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 14, "evidence_page_end": 15 },
                { "evidence_id": 3, "evidence_name": "Procuração", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 16, "evidence_page_end": 16 },
                { "evidence_id": 4, "evidence_name": "Declaração de Hipossuficiência", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 17, "evidence_page_end": 17 },
                { "evidence_id": 5, "evidence_name": "Documento de Identidade", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 18, "evidence_page_end": 20 },
                { "evidence_id": 6, "evidence_name": "Comprovante de residência", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 21, "evidence_page_end": 21 },
                { "evidence_id": 7, "evidence_name": "Carteira de trabalho", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 22, "evidence_page_end": 22 },
                { "evidence_id": 8, "evidence_name": "Comprovante de Inscrição CPF", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 23, "evidence_page_end": 24 },
                { "evidence_id": 9, "evidence_name": "Consulta restituição IRPF", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 25, "evidence_page_end": 26 },
                { "evidence_id": 10, "evidence_name": "Declaração do Imposto sobre a Renda Retido na Fonte", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 27, "evidence_page_end": 27 },
                { "evidence_id": 11, "evidence_name": "Certidão Negativa de Débitos Trabalhistas", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 28, "evidence_page_end": 28 },
                { "evidence_id": 12, "evidence_name": "Certidão Negativa de Débitos", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 29, "evidence_page_end": 29 },
                { "evidence_id": 13, "evidence_name": "Regulamento do Fundo de Investimento", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 41, "evidence_page_end": 83 },
                { "evidence_id": 14, "evidence_name": "Termo de Transferência da sede social", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 111, "evidence_page_end": 111 },
                { "evidence_id": 15, "evidence_name": "Procuração", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 114, "evidence_page_end": 116 },
                { "evidence_id": 16, "evidence_name": "Substabelecimento", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 128, "evidence_page_end": 128 },
                { "evidence_id": 17, "evidence_name": "Carta de Preposição", "evidence_flaw": "Sem inconsistências", "evidence_page_init": 134, "evidence_page_end": 134 }
            ]
        }