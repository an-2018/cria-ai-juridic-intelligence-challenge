from pydantic import BaseModel


class Settings(BaseModel):
    # TODO: Add application settings, variables, and constants
    APP_NAME: str = "ProcessDataExtract"
    APP_VERSION: str = "1.0.0"
    pass

settings = Settings()