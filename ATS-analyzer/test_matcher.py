# test_matcher.py  ← raiz do projeto
from core.matcher import match_resume_to_job

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

result = match_resume_to_job(resume_text, job_text)

skills = result["skills"]
print(f"✅ Skills que batem:   {skills['matched']}")
print(f"❌ Skills que faltam:  {skills['missing']}")
print(f"➕ Skills extras:      {skills['extra']}")
print(f"📊 Match rate:         {skills['match_rate'] * 100:.0f}%")
print(f"🎯 Senioridade:        {result['seniority']['detail']}")
print(f"📅 Experiência:        {result['experience']['detail']}")