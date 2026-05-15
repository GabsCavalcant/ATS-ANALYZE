# core/nlp.py

"""
Módulo de NLP (Processamento de Linguagem Natural).

Responsabilidade: receber o texto limpo do currículo (ou da vaga)
e extrair informações estruturadas dele.

Fase 1: extração baseada em keywords e regex (sem modelo de linguagem).
Fase 2 (futura): substituir por spaCy para extração semântica real.
"""

import re
from core.parser import parse_resume


# ---------------------------------------------------------------------------
# Base de conhecimento (expanda conforme necessário)
# ---------------------------------------------------------------------------

SKILLS_DATABASE = {
    "linguagens": [
        "python", "javascript", "typescript", "java", "c#", "c++",
        "go", "rust", "kotlin", "swift", "php", "ruby", "scala",
        "r", "matlab", "sql",
    ],
    "frameworks_backend": [
        "fastapi", "django", "flask", "express", "spring", "nestjs",
        "laravel", "rails", "gin", "fiber",
    ],
    "frameworks_frontend": [
        "react", "vue", "angular", "svelte", "next.js", "nuxt",
        "tailwind", "bootstrap",
    ],
    "dados_e_ia": [
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
        "keras", "spacy", "nltk", "matplotlib", "seaborn",
        "machine learning", "deep learning", "nlp",
    ],
    "devops_e_cloud": [
        "docker", "kubernetes", "aws", "gcp", "azure", "terraform",
        "ansible", "jenkins", "github actions", "ci/cd", "linux",
    ],
    "bancos_de_dados": [
        "postgresql", "mysql", "mongodb", "redis", "sqlite",
        "elasticsearch", "cassandra", "dynamodb",
    ],
    "ferramentas": [
        "git", "github", "gitlab", "jira", "figma", "postman",
        "vs code", "docker compose",
    ],
}

SENIORITY_KEYWORDS = {
    "junior": ["júnior", "junior", "estagiário", "trainee", "entry level", "iniciante"],
    "mid":    ["pleno", "mid-level", "mid level", "intermediário"],
    "senior": ["sênior", "senior", "sr.", "especialista", "lead", "principal", "staff"],
}


# ---------------------------------------------------------------------------
# Funções de extração
# ---------------------------------------------------------------------------

def extract_skills(text: str) -> dict:
    """
    Varre o texto procurando skills conhecidas da nossa base.

    Por que .lower()?
    - "Python", "PYTHON" e "python" são a mesma skill.
    - Normalizar garante que não percamos matches por capitalização.

    Por que retornar dict por categoria?
    - Facilita o matcher comparar categorias específicas com a vaga.
    - Ex: vaga pede "Python" → verificamos só em 'linguagens', não tudo.

    Returns:
        Dict onde chave = categoria e valor = lista de skills encontradas.
        Ex: {"linguagens": ["python", "sql"], "devops_e_cloud": ["docker"]}
    """
    text_lower = text.lower()
    found = {}

    for category, skills in SKILLS_DATABASE.items():
        matches = []
        for skill in skills:
            # \b = word boundary: garante que "r" não bate em "frameworks"
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                matches.append(skill)

        if matches:  # Só adiciona categoria se tiver ao menos 1 match
            found[category] = matches

    return found


def extract_years_of_experience(text: str) -> int | None:
    """
    Tenta encontrar anos de experiência mencionados no texto.

    Padrões que reconhecemos:
    - "3 anos de experiência"
    - "5+ anos"
    - "mais de 2 anos"
    - "dois anos" (por extenso — versão básica)

    Por que retornar None em vez de 0?
    - 0 anos é uma informação (estagiário, sem experiência).
    - None significa "não mencionado" — são coisas diferentes.

    Returns:
        Número de anos como int, ou None se não encontrado.
    """
    text_lower = text.lower()

    # Padrão numérico: "3 anos", "3+ anos", "+ de 3 anos", "mais de 3 anos"
    numeric_pattern = r'(?:mais\s+de\s+|[\+]?\s*)?(\d+)\s*\+?\s*anos'
    match = re.search(numeric_pattern, text_lower)

    if match:
        return int(match.group(1))

    # Padrão por extenso (básico — os mais comuns)
    written_numbers = {
        "um ano": 1, "dois anos": 2, "três anos": 3,
        "quatro anos": 4, "cinco anos": 5, "seis anos": 6,
        "sete anos": 7, "oito anos": 8, "dez anos": 10,
    }
    for phrase, value in written_numbers.items():
        if phrase in text_lower:
            return value

    return None


def extract_seniority(text: str) -> str:
    """
    Infere o nível de senioridade com base em keywords.

    Ordem de verificação importa: verificamos 'senior' antes de 'junior'
    porque "Sênior" é mais específico e menos comum como falso positivo.

    Returns:
        'junior', 'mid', 'senior' ou 'not_specified'.
    """
    text_lower = text.lower()

    for level, keywords in SENIORITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return level

    return "not_specified"


def extract_email(text: str) -> str | None:
    """
    Extrai o primeiro e-mail encontrado no texto.

    O regex cobre formatos comuns:
    - usuario@dominio.com
    - usuario.nome@empresa.com.br
    """
    pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_linkedin(text: str) -> str | None:
    """
    Extrai URL ou handle do LinkedIn, se presente.
    """
    pattern = r'linkedin\.com/in/[a-zA-Z0-9\-_]+'
    match = re.search(pattern, text.lower())
    return match.group(0) if match else None


# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------

def analyze_text(text: str) -> dict:
    """
    Orquestra todas as extrações e retorna um perfil estruturado.

    Esta é a função que as outras camadas (matcher, scorer) vão chamar.
    Elas não precisam saber como extraímos — só precisam do resultado.

    Args:
        text: Texto limpo (currículo ou descrição de vaga).

    Returns:
        Dicionário com todas as informações extraídas.
    """
    skills = extract_skills(text)

    # Achata todas as skills em uma lista única (útil pro matcher)
    all_skills_flat = [
        skill
        for skill_list in skills.values()
        for skill in skill_list
    ]

    return {
        "skills_by_category": skills,
        "skills": all_skills_flat,         # Lista plana para comparação rápida
        "total_skills_found": len(all_skills_flat),
        "years_experience": extract_years_of_experience(text),
        "seniority": extract_seniority(text),
        "email": extract_email(text),
        "linkedin": extract_linkedin(text),
    }


def analyze_resume(file_path: str) -> dict:
    """
    Atalho conveniente: recebe caminho do PDF e retorna análise completa.

    Combina parser + nlp em uma única chamada.
    Útil para testes rápidos e para o endpoint da API futuramente.
    """
    parsed = parse_resume(file_path)

    if parsed["status"] == "error":
        return {"status": "error", "message": parsed["message"]}

    analysis = analyze_text(parsed["text"])
    analysis["source"] = parsed["source"]
    analysis["status"] = "success"

    return analysis