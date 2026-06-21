from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from core.parser import parse_resume
from core.nlp import analyze_text
from core.matcher import match_resume_to_job
from core.scorer import calculate_score
from core.feedback import generate_feedback

app = FastAPI(
    title="ATS Analyzer API",
    description="API para análise de currículos vs descrição de vaga",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "ATS Analyzer API está rodando!"}

@app.post("/analyze")
async def analyze(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    filename = resume.filename.lower()
    if not filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um PDF.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await resume.read())
        tmp_path = tmp.name

    try:
        # 1. Extrai texto do PDF
        parsed = parse_resume(tmp_path)
        if parsed["status"] == "error":
            raise HTTPException(status_code=400, detail=parsed["message"])

        resume_text = parsed["text"]
        print("=== TEXTO EXTRAÍDO ===")
        print(resume_text[:200])
        print("=== FIM ===")
        # 2. Compara currículo com a vaga
        match_result = match_resume_to_job(resume_text, job_description)

        # 3. Calcula o score
        score_result = calculate_score(match_result)

        # 4. Gera feedback com IA
        feedback = generate_feedback(score_result, match_result)
        print("=== RESULTADO MATCH ===")
        print(match_result)
        print("=== FIM ===")
        return {
            "score": score_result,
            "match": match_result,
            "feedback": feedback
        }
    finally:
        os.unlink(tmp_path)