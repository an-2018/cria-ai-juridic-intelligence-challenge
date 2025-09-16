from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # TODO: Add application settings, variables, and constants
    APP_NAME: str = "ProcessDataExtract"
    APP_VERSION: str = "1.0.0"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash"
    DYNAMODB_TABLE_NAME: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()