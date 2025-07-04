from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(req: QuestionRequest):
    question = req.question

    if "hello" in question.lower():
        return {"answer": "Hi there!"}
    elif "your name" in question.lower():
        return {"answer": "I'm a FastAPI bot."}
    else:
        return {"answer": f"You asked: '{question}'. I will get back to you!"}
