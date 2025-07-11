
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "✅ Trudata backend is running"}

@app.post("/api/validate")
async def validate(request: Request):
    payload = await request.json()
    print("Received:", payload)
    return {
        "message": "Validation complete",
        "input_summary": payload
    }
