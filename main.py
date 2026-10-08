from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()
class AskRequest(BaseModel):
    question: str
    model: str = "gemini-3.8-flash-high"
@app.post("/ask")
def ask(request: AskRequest):
    question = request.question
    question = question.strip()
    model = request.model
    if not question:
        return {
            "answer": "问题不能为空，请重新输入"
        }
    answer = run_agent(question,model)
    return{
        "answer": answer
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }