from abc import ABC, abstractmethod


class ILlmClient(ABC):
    @abstractmethod
    def extract_data_from_pdf(self, pdf_binary: str) -> dict:
        """
        Extracts structured data from a PDF file binary.
        
        Args:
            pdf_binary: the pdf file in binary format.
        
        Returns:
            a dictionary with the information extracted from the pdf document ('resume', 'timeline', 'evidence').
        """
        pass