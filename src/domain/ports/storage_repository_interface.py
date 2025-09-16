from abc import ABC, abstractmethod


class IStorageRepository(ABC):
    @abstractmethod
    def save(self, case_id: str, data: dict) -> None:
        """
        Saves the extracted data from the pdf document into the storage service

        Args:
            case_id: the unique id of the file
            data: the strutured data extracted from the pdf document
        Returns:
            None
        """
        pass