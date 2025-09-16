# Legal Document Analysis and Data Extraction with Gemini API

This project is a serverless application that provides an API to analyze legal documents from a PDF URL. It uses Google's Gemini API service to extract structured data (a case summary, a chronological timeline, and a list of evidence) and stores the results in a MongoDB database.

## Architecture

The application follows a simple, event-driven serverless architecture:

1.  A client sends a `POST` request with a JSON payload containing a `pdf_url` and the `case_id` to the API endpoint `/extract` (current version only runs locally, missing fix for the deployed version).
2.  API Gateway triggers an **AWS Lambda** function.
3.  The Lambda function:
    a. Downloads the PDF file from the provided URL.
    b. Uploads the file to the **Google Gemini API** for analysis.
    c. Receives the structured JSON data back from Gemini.
    d. Saves the extracted data to a **MongoDB** database.
4.  The Lambda function returns the extracted JSON data to the client.

```
  Client
    │
    │ POST /extract
    ▼
┌──────────────────┐
│ Amazon API Gateway │
└──────────────────┘
    │
    │ Triggers
    ▼
┌──────────────────┐
│   AWS Lambda     │───►┌───────────────────┐
│ (process_data)   │    │ Google Gemini API │
└──────────────────┘    └───────────────────┘
    │
    │ Saves data
    ▼
┌──────────────────┐
│     MongoDB      │
└──────────────────┘
```

Note: At current version the api can be run using the uvicorn package for fastapi.

## Prerequisites

Before begin, ensure the following installed and configured:

*   **AWS CLI**: Configure AWS credentials.
*   **AWS SAM CLI**: For building, testing, and deploying the application.
*   **Docker**: Required for building Lambda dependencies and running local services.
*   **Python 3.12**: The runtime for the Lambda function.
*   **Google Gemini API Key**: Get one from Google AI Studio.

## Project Setup

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd cria-ai-juridic-intelligence-challenge
    ```

2.  **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    The project's Python dependencies are listed in `requirements.txt` file. The `pip install -r requirements.txt` command will install them.

4.  **Configure Environment Variables for Local Testing**

    Create a file named `.env.json` in the project root. This file will provide environment variables for local testing. An example of the variables is provided in `.env.example`

    ```
    GEMINI_API_KEY="api-key"
    GEMINI_MODEL_NAME="gemini-2.0-flash"
    MONGODB_DB_NAME="process_data_db"
    MONGODB_URI="mongodb://localhost:27017/"
    ```

    - Replace `API_KEY` with actual gemini API key from https://aistudio.google.com/.


## Local Development and Testing

1.  **Start Local MongoDB**
    The docker compose contains service for the mongo database and localstack configuration (the free version of localstack doenst provide storage services).
    ```bash
    docker compose up -d
    ```

2.  **Build the Application**
    The `--use-container` flag builds the function inside a Docker container that mimics the Lambda environment.
    ```bash
    sam build --use-container
    ```

3.  **Run the API Locally**
    Running the following command at the root of the project starts the api server and hot-reloads on code changes.
    ```bash
    python -m src.main
    ```
    A swagger documentation that comes with the fastapi implementation will be available at `http://127.0.0.1:8000/docs`.

4.  **Invoke the Function Locally**
    Send a request to the local endpoint using `curl` or an API client like Postman.
    ```bash
    curl -X POST http://127.0.0.1:8000/extract \
    -H "Content-Type: application/json" \
    -d '{"pdf_url": "URL_TO_LEGAL_DOCUMENT.pdf", "case_id": "CASE_ID"}'
    ```

## Deployment to AWS

1.  **Guided Deployment**
    The first deploy, can use the `--guided` flag. SAM will prompt for deployment parameters.

    ```bash
    sam deploy --guided
    ```

    It will ask for:
    - **Stack Name**: A unique name for CloudFormation stack (e.g., `legal-doc-analyzer`).
    - **AWS Region**: The region to deploy to (e.g., `us-east-1`).
    - **Parameter `GeminiApiKey`**: **Enter Google Gemini API key**.
    - **Parameter `MongoDbUri`**: The connection string for the MongoDB (e.g., a MongoDB Atlas URI).
    - **Confirm changes before deploy**: Answer `y`.
    - **Allow SAM CLI IAM role creation**: Answer `y`.

    SAM will save the choices in `samconfig.toml` for future deployments.

2.  **Subsequent Deployments**
    After the first deployment, we can simply run:
    ```bash
    sam deploy
    ```

## Cleanup

To delete the deployed application and all associated AWS resources, run:
```bash
sam delete
```

## Future works

- Implement unit and integration tests
- Fix configuration for lambda deployment
- Add more validations for data input and response from gemini
- Test best model for file analysis
- Explorre the possibility of getting metrics and XAI features from the model output to evaluate possible alucinations or inacurate data output
