import logging
from pymongo import MongoClient
from src.infrastruture.configs.app_config import settings
from src.domain.ports.storage_repository_interface import IStorageRepository


class MongoDBRepository(IStorageRepository):
    """Implementation of the storage repository using MongoDB"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.client = MongoClient(settings.MONGODB_URI)
            self.db = self.client[settings.MONGODB_DB_NAME]
            self.collection = self.db["process_data"]
            self.logger.info("Connected to MongoDB")
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def save(self, case_id: str, data: dict) -> None:
        """Saves the extracted data in the mongo database."""
        try:
            self.logger.info(f"Saving data for case_id: {case_id} to MongoDB")
            self.collection.update_one(
                {"case_id": case_id},
                {"$set": data},
                upsert=True
            )
            self.logger.info(f"Data for case_id: {case_id} saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save data for case_id {case_id}: {e}")
            raise