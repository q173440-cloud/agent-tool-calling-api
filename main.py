from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()
class AskRequest(BaseModel):
    question: str
@app.post("/ask")
def ask(request: AskRequest):
    question = request.question
    answer = run_agent(question)
    return{
        "answer": answer
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }