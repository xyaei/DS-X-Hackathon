from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm.api import router as career_router

app = FastAPI(title="Main API")

# CORS (mirrors your previous open policy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the LLM/career router at /career
app.include_router(career_router)

@app.get("/")
def root():
    return {"message": "Main API is running", "routes": ["GET /", "mounted: /career/*"]}

# Run with:
#   cd backend
#   uvicorn server:app --reload --port 8000
