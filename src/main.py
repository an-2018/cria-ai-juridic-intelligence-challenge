import sys
from fastapi import FastAPI
from logging.config import dictConfig
from src.routes.process__data_routes import router as process_data_router
import src.infrastruture.configs.log_config  # logging configuratio
# from mangum import Mangum # aws lambda
from src.infrastruture.configs.app_config import settings

app = FastAPI(title="Cria AI Juridic Intelligence Challenge", version="1.0.0")
app.include_router(process_data_router)

# handler = Mangum(app) # aws lambda

if __name__ == "__main__":
    import uvicorn
    print("--- App Settings ---")
    print(f"GEMINI_API_KEY loaded: {bool(settings.GEMINI_API_KEY)}")
    print(f"DYNAMODB_TABLE_NAME: {settings.DYNAMODB_TABLE_NAME}")
    print("--------------------")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True,  reload_dirs=["src"])