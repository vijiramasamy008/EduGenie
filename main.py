
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# Project folder location
BASE_DIR = Path(__file__).resolve().parent

# Create FastAPI application
app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)

# Frontend configuration
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# Request models
class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000)


class QuizRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000)
    num_questions: int = Field(default=3, ge=1, le=10)


class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=500)
    level: str = Field(default="Beginner", max_length=50)


# Homepage
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


# Health check
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": "EduGenie",
    }


# Question and Answer
@app.post("/qa")
async def qa(payload: TextRequest):
    try:
        answer = answer_question(payload.text)
        return {"answer": answer}
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# Explain a topic
@app.post("/explain")
async def explain(payload: TextRequest):
    try:
        explanation = explain_topic(payload.text)
        return {"explanation": explanation}
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# Generate quiz
@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        questions = generate_quiz(
            payload.text,
            payload.num_questions,
        )
        return {"quiz": questions}
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# Summarize educational text
@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        summary = summarize_text(payload.text)
        return {"summary": summary}
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# Personalized learning path
@app.post("/learn/recommendations")
async def recommendations(
    payload: LearningPathRequest,
):
    try:
        learning_path = get_learning_recommendations(
            payload.topic,
            payload.level,
        )
        return {"learning_path": learning_path}
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

        