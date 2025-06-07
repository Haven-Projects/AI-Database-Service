from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from langchain_helper import get_few_shot_db_chain, safe_chain_call
import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize limiter properly
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="AI Database Query Service", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Initialize the chain once at startup
chain = None

@app.on_event("startup")
async def startup_event():
    global chain
    try:
        chain = get_few_shot_db_chain()
        print("AI Database Service initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize service: {e}")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    status: str

@app.get("/")
async def root():
    return {"message": "AI Database Query Service is running!"}

@app.post("/query", response_model=QueryResponse)
@limiter.limit("10/minute")  # Now properly configured
async def query_database(request: Request, query_request: QueryRequest):
    if not chain:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        result = safe_chain_call(chain, query_request.question)
        print(f"Result from safe_chain_call: {result}")
        return QueryResponse(answer=result, status="success")
    except Exception as e:
        print(f"Error in query_database: {e}")
        return QueryResponse(answer="Sorry, can't help with that.", status="error")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Database Query"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)