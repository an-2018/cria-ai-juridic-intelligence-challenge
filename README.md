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

![swagger docs](docs/image-1.png)


4.  **Invoke the Function Locally**
    Send a request to the local endpoint using `curl` or an API client like Postman.
    ```bash
    curl -X POST http://127.0.0.1:8000/extract \
    -H "Content-Type: application/json" \
    -d '{"pdf_url": "URL_TO_LEGAL_DOCUMENT.pdf", "case_id": "CASE_ID"}'
    ```

Example response:

![example response](docs/image-2.png)

```json
{
  "case_id": "0809090-86.2024999.12.0721",
  "resume": "José Ribamar Alves Filho initiated a lawsuit against FUNDO DE INVESTIMENTO EM DIREITOS CREDITORIOS NAO PADRONIZADOS NPL II, seeking a declaration of non-existent debt, moral damages of R$ 35,000.00, and a preliminary injunction. The plaintiff claims an undue negative credit registration (R$ 892.61, due 2021-01-22) by FIDIC NPL II, which he asserts is fraudulent and unknown. The court granted preliminary injunction and free legal assistance on 2024-10-23, ordering the suspension of the plaintiff's name from credit protection agencies. A conciliation hearing was scheduled for 2025-03-24. An attempt to serve summons to the defendant failed on 2025-01-17 (marked as 'Absent'). The defendant subsequently filed documents appointing legal representatives on 2025-03-21. The conciliation hearing proceeded as scheduled on 2025-03-24 with both parties represented, but no agreement was reached. The defendant was then instructed to present their defense within 15 days.",
  "timeline": [
    {
      "event_id": 0,
      "event_name": "Vencimento da Dívida Contestada",
      "event_description": "Data de vencimento da dívida de R$ 892,61 contestada pelo Autor como inexistente.",
      "event_date": "2021-01-22",
      "event_page_init": 2,
      "event_page_end": 2
    },
    {
      "event_id": 1,
      "event_name": "Declaração de Alteração de Endereço do Fundo",
      "event_description": "O FUNDO DE INVESTIMENTO EM DIREITOS CREDITORIOS NAO PADRONIZADOS NPL II declara alteração de sua sede social, com eficácia a partir desta data, sendo assinada digitalmente por seus representantes.",
      "event_date": "2023-07-03",
      "event_page_init": 111,
      "event_page_end": 113
    },
    {
      "event_id": 2,
      "event_name": "Substabelecimento de Poderes (Réu - Recovery do Brasil)",
      "event_description": "Substabelecimento de poderes de RECOVERY DO BRASIL CONSULTORIA S.A. para vários advogados, incluindo SUELLEN NOGUEIRA VENTURA e outros.",
      "event_date": "2024-05-20",
      "event_page_init": 122,
      "event_page_end": 125
    },
    {
      "event_id": 3,
      "event_name": "Descoberta de Negativação Indevida",
      "event_description": "O Requerente foi surpreendido com a negativa de empréstimo e posterior descoberta de uma negativação indevida junto ao SPC.",
      "event_date": "2024-09-01",
      "event_page_init": 2,
      "event_page_end": 2
    },
    {
      "event_id": 4,
      "event_name": "Assinatura da Procuração do Autor",
      "event_description": "JOSÉ RIBAMAR ALVES FILHO outorga procuração 'ad judicia et extra' à advogada Tânia Cristina Xisto Timoteo.",
      "event_date": "2024-09-16",
      "event_page_init": 16,
      "event_page_end": 16
    },
    {
      "event_id": 5,
      "event_name": "Assinatura da Declaração de Hipossuficiência",
      "event_description": "JOSÉ RIBAMAR ALVES FILHO declara não possuir condições de arcar com as custas do processo sem prejuízo do seu sustento.",
      "event_date": "2024-09-16",
      "event_page_init": 17,
      "event_page_end": 17
    },
    {
      "event_id": 6,
      "event_name": "Emissão do Relatório de Crédito (Crednet Light)",
      "event_description": "Consulta do CPF do Autor que resultou na emissão do relatório de crédito Crednet Light, evidenciando as negativações, incluindo a dívida contestada.",
      "event_date": "2024-10-03",
      "event_page_init": 14,
      "event_page_end": 15
    },
    {
      "event_id": 7,
      "event_name": "Ajuizamento da Ação",
      "event_description": "JOSÉ RIBAMAR ALVES FILHO propõe AÇÃO DECLARATÓRIA DE INEXISTÊNCIA DE DÉBITOS C/C INDENIZAÇÃO POR DANOS MORAIS e pedido de tutela de urgência.",
      "event_date": "2024-10-22",
      "event_page_init": 1,
      "event_page_end": 13
    },
    {
      "event_id": 8,
      "event_name": "Registro de Ação no Sistema Judiciário",
      "event_description": "O sistema judiciário certifica a entrada da ação e que não há processos repetidos relacionados ao processo 0809090-86.2024.8.12.0021.",
      "event_date": "2024-10-22",
      "event_page_init": 30,
      "event_page_end": 30
    },
    {
      "event_id": 9,
      "event_name": "Retificação de Nome no Cadastro do Processo",
      "event_description": "O nome do Autor foi retificado no cadastro do processo de 'Jose Ribamar Alves Filho' para 'José Ribamar Alves Filho'.",
      "event_date": "2024-10-23",
      "event_page_init": 31,
      "event_page_end": 31
    },
    {
      "event_id": 10,
      "event_name": "Decisão Interlocutória (Deferimento de Tutela de Urgência e Justiça Gratuita)",
      "event_description": "A Juíza defere o pedido de tutela provisória de urgência para suspender o nome da autora do SERASA/SCPC pela dívida representada nesses autos e concede o benefício da justiça gratuita.",
      "event_date": "2024-10-23",
      "event_page_init": 32,
      "event_page_end": 34
    },
    {
      "event_id": 11,
      "event_name": "Remessa de Relação para Publicação",
      "event_description": "Certidão atesta que o ato de deferimento da tutela de urgência e justiça gratuita foi encaminhado para publicação.",
      "event_date": "2024-11-14",
      "event_page_init": 35,
      "event_page_end": 35
    },
    {
      "event_id": 12,
      "event_name": "Publicação da Decisão Interlocutória",
      "event_description": "O ato de deferimento da tutela de urgência e justiça gratuita foi publicado no Diário da Justiça nº 5529.",
      "event_date": "2024-11-19",
      "event_page_init": 36,
      "event_page_end": 36
    },
    {
      "event_id": 13,
      "event_name": "Designação de Audiência de Conciliação",
      "event_description": "Designada Sessão de Conciliação para 2025-03-24 às 14:20h, na Sala CEJUSC. Informações para audiência virtual também são fornecidas.",
      "event_date": "2024-11-27",
      "event_page_init": 37,
      "event_page_end": 39
    },
    {
      "event_id": 14,
      "event_name": "Emissão de Carta de Citação e Intimação",
      "event_description": "Carta de citação e intimação emitida para o Réu comparecer à audiência de conciliação em 2025-03-24.",
      "event_date": "2025-01-07",
      "event_page_init": 131,
      "event_page_end": 131
    },
    {
      "event_id": 15,
      "event_name": "Tentativa de Citação do Réu",
      "event_description": "Tentativa de entrega da carta de citação ao Réu em 2025-01-17, com a observação 'Ausente'.",
      "event_date": "2025-01-17",
      "event_page_init": 132,
      "event_page_end": 132
    },
    {
      "event_id": 16,
      "event_name": "Juntada de Carta de Preposição e Substabelecimento do Réu",
      "event_description": "O Fundo de Investimento Em Direitos Creditórios Não Padronizados NPL II protocola carta de preposição e substabelecimento de advogados, nomeando Daniel Nogueira de Carvalho e Nadir Alcides Oliveira Júnior como seus representantes para a audiência de conciliação.",
      "event_date": "2025-03-21",
      "event_page_init": 133,
      "event_page_end": 138
    },
    {
      "event_id": 17,
      "event_name": "Audiência de Conciliação",
      "event_description": "Realizada audiência de conciliação com a presença de representantes de ambas as partes (Autor representado pela advogada e Réu pelo preposto e advogado), mas sem acordo. O Réu foi notificado para apresentar contestação em 15 dias.",
      "event_date": "2025-03-24",
      "event_page_init": 139,
      "event_page_end": 140
    }
  ],
  "evidence": [
    {
      "evidence_id": 0,
      "evidence_name": "Relatório de Consulta Crednet Light",
      "evidence_flaw": "Contém registro de dívida (\"Pendência Pefin\") de R$ 892,61 em nome do Autor, com vencimento em 22/01/2021, que é contestada como inexistente/fraudulenta.",
      "evidence_page_init": 14,
      "evidence_page_end": 15
    },
    {
      "evidence_id": 1,
      "evidence_name": "Procuração \"Ad Judicia et Extra\" (Autor)",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 16,
      "evidence_page_end": 16
    },
    {
      "evidence_id": 2,
      "evidence_name": "Declaração de Hipossuficiência (Autor)",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 17,
      "evidence_page_end": 17
    },
    {
      "evidence_id": 3,
      "evidence_name": "Documento de Identidade (RG) do Autor",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 19,
      "evidence_page_end": 20
    },
    {
      "evidence_id": 4,
      "evidence_name": "Fatura Neoenergia",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 21,
      "evidence_page_end": 21
    },
    {
      "evidence_id": 5,
      "evidence_name": "Carteira de Trabalho Digital do Autor",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 22,
      "evidence_page_end": 22
    },
    {
      "evidence_id": 6,
      "evidence_name": "Comprovante de Situação Cadastral no CPF do Autor",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 23,
      "evidence_page_end": 24
    },
    {
      "evidence_id": 7,
      "evidence_name": "Consulta Restituição IRPF do Autor",
      "evidence_flaw": "\"Não há informação para o exercício informado\", o que corrobora a alegação de baixa renda/inexistência de restituição.",
      "evidence_page_init": 25,
      "evidence_page_end": 26
    },
    {
      "evidence_id": 8,
      "evidence_name": "Declaração do Imposto sobre a Renda Retido na Fonte - Dirf",
      "evidence_flaw": "\"Não Consta Entrega de Declarações\", o que corrobora a alegação de baixa renda/nenhuma retenção de imposto na fonte.",
      "evidence_page_init": 27,
      "evidence_page_end": 27
    },
    {
      "evidence_id": 9,
      "evidence_name": "Certidão Negativa de Débitos Trabalhistas do Autor",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 28,
      "evidence_page_end": 28
    },
    {
      "evidence_id": 10,
      "evidence_name": "Certidão Negativa de Débitos Relativos aos Tributos Federais e à Dívida Ativa da União do Autor",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 29,
      "evidence_page_end": 29
    },
    {
      "evidence_id": 11,
      "evidence_name": "Regulamento do FUNDO DE INVESTIMENTO EM DIREITOS CREDITORIOS NAO PADRONIZADOS NPL II e Anexos",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 41,
      "evidence_page_end": 110
    },
    {
      "evidence_id": 12,
      "evidence_name": "Declaração de Alteração de Endereço do FUNDO DE INVESTIMENTO EM DIREITOS CREDITORIOS NAO PADRONIZADOS NPL II",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 111,
      "evidence_page_end": 113
    },
    {
      "evidence_id": 13,
      "evidence_name": "Procuração com Revogação (Réu)",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 114,
      "evidence_page_end": 120
    },
    {
      "evidence_id": 14,
      "evidence_name": "Substabelecimento de Poderes (Réu - Recovery do Brasil)",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 122,
      "evidence_page_end": 125
    },
    {
      "evidence_id": 15,
      "evidence_name": "Carta de Preposição (Réu)",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 133,
      "evidence_page_end": 134
    },
    {
      "evidence_id": 16,
      "evidence_name": "Substabelecimento de Poderes (Réu - Nadir Alcides Oliveira Júnior)",
      "evidence_flaw": "Sem inconsistências",
      "evidence_page_init": 135,
      "evidence_page_end": 138
    }
  ],
  "persisted_at": "2025-09-16T18:57:47.718540Z"
}
```


Using MongoCompass for instance we can validate the persistence of the extracted data:
![mongo-compass data storage](docs/image-3.png)

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


## Issues

- Currently it returns the following error while deploying locally using the `samlocal deploy --guided` command:

![error log](docs/image.png)

- Some local tests presented the following error:
```
google.genai.errors.ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'The model is overloaded. Please try again later.', 'status': 'UNAVAILABLE'}}
```
Changing and choosing another available model may solve the issue temporarily, in the .env configuratin file
```
GEMINI_MODEL_NAME="gemini-2.5-flash"
```

- the provided pdf_url currently only accepts public urls, 403 error codes may be returned if no open access to the pdf is available