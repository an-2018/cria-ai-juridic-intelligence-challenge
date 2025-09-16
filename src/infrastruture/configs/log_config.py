import sys
from datetime import datetime
from src.infrastruture.configs.app_config import settings
from pydantic import BaseModel
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        # logging.FileHandler('app.log')
    ]
)
