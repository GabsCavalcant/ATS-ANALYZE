# test_feedback.py  ← raiz do projeto
from core.matcher import match_resume_to_job
from core.scorer import calculate_score
from core.feedback import generate_feedback

resume_text = """
João Silva — Desenvolvedor Python Sênior
joao@email.com

5 anos de experiência com Python, FastAPI, Docker e PostgreSQL.
Conhecimento em AWS e GitHub Actions.
"""

job_text = """
Vaga: Desenvolvedor Python Pleno

Requisitos:
- Python, FastAPI, PostgreSQL
- Docker e Kubernetes
- AWS ou GCP
- 3 anos de experiência
"""

match_result = match_resume_to_job(resume_text, job_text)
score_result = calculate_score(match_result)
feedback = generate_feedback(score_result, match_result)

if feedback["status"] == "success":
    print(f"\n{'='*50}")
    print(f"  SCORE: {feedback['score']}/100 — {feedback['label']}")
    print(f"{'='*50}\n")
    print(feedback["feedback"])
else:
    print(f"❌ Erro: {feedback['message']}")