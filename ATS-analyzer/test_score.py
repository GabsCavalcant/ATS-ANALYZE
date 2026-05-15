# test_scorer.py  ← raiz do projeto
from core.matcher import match_resume_to_job
from core.scorer import calculate_score

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

print(f"\n{'='*40}")
print(f"  SCORE FINAL: {score_result['score']}/100 — {score_result['label']}")
print(f"{'='*40}")
print(f"  Skills:      {score_result['breakdown']['skills']}/100  (peso 60%)")
print(f"  Experiência: {score_result['breakdown']['experience']}/100  (peso 25%)")
print(f"  Senioridade: {score_result['breakdown']['seniority']}/100  (peso 15%)")
print(f"{'='*40}\n")