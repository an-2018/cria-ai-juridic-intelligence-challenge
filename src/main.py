from fastapi import FastAPI
from src.routes.process__data_routes import router as process_data_router
# from mangum import Mangum # aws lambda

app = FastAPI(title="Cria AI Juridic Intelligence Challenge", version="1.0.0")
app.include_router(process_data_router)

# handler = Mangum(app) # aws lambda


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)