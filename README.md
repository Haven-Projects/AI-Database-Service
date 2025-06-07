# AI-Database-Service

AI-Database-Service is a tool that translates natural language questions into SQL queries, executes them on a connected database, and returns the results. This enables users to interact with databases using plain English, making data access more intuitive and accessible.

## Tech Stack

- **API End-Point:** Fast API
- **GEN AI:** Google Gemini API
- **AI Libraries:** LangChain, Huggingface Sentence Transformers, ChromaDB Vector Stores
- **Database:** MariaDB 
- **Environment Management:** dotenv

## Technical Architecture

1. **API Layer:** Receives natural language queries via REST endpoints.
2. **NLP Processing:** Uses an Gen AI model to convert natural language into SQL.
3. **Database Layer:** Executes the generated SQL query on the configured database.
4. **Response Layer:** Returns the query results to the user.

```
   User Input (Natural Language)
    |
    v
   REST API Endpoint
    |
    v
   GEN AI Model (NLP → SQL)
    |
    v
   SQL Query Execution
    |
    v
   Results Returned
```

## Setting Up the `.env` File

Create a `.env` file in the project root with the following variables:

```
API_KEY=your_gemini_api_key_here
DB_USER=appWorker
DB_PASS=password
DB_HOST=localhost
DB_NAME=app
```


