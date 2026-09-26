from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Knowledge Retrieval Platform",
    version="0.1.0"
)

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "knowledge-retrieval"
    }