"""
Módulo de scoring.

Responsabilidade: receber o resultado do matcher e transformar
em um score final de 0 a 100, com breakdown por categoria.

Não sabe nada sobre PDFs, textos ou comparações.
Só recebe números e devolve números.
"""

#config de pesos

WEIGHTS = {
    "skills": 0.6,
    "seniority": 0.25,
    "experience": 0.15,
}

assert sum(WEIGHTS.values()) == 1.0, "Os pesos devem somar 1.0"


#funções de scoring por categorias

def score_skills(skills_result: dict) -> float:
    
    return skills_result['match_rate'] * 100

def score_experience(experience_result: dict) -> float:
    """
    Converte o resultado de experiência em score 0–100.

    Lógica:
    - Não especificado → 70 (benefício da dúvida)
    - Candidato tem mais anos que o exigido → 100
    - Candidato tem exatamente o exigido → 100
    - Candidato tem menos → penaliza proporcionalmente

    Por que não dar 0 quando falta experiência?
    Porque 1 ano abaixo do exigido é muito diferente de 5 anos abaixo.
    A penalização gradual é mais justa e realista.

    Returns:
        Float entre 0 e 100.
    """
    if experience_result["detail"] == "not_specified":
        return 70.0   # Benefício da dúvida quando não mencionado

    gap = experience_result["gap"]

    if gap >= 0:
        return 100.0  # Tem o suficiente ou mais

    # Penaliza 15 pontos por ano abaixo do exigido
    # Ex: 1 ano abaixo → 85 | 2 anos abaixo → 70 | 7+ anos abaixo → 0
    penalty = abs(gap) * 15
    return max(0.0, 100.0 - penalty)

def score_seniority(seniority_result: dict) -> float:
    """
    Converte o resultado de senioridade em score 0–100.

    Lógica:
    - Não especificado → 70 (benefício da dúvida)
    - Candidato no nível exigido → 100
    - Candidato acima do exigido → 100
    - Candidato abaixo do exigido → penaliza

    Penalização:
    - Se candidato é "below" → 50 pontos
    - Se "not_specified" → 70 pontos
    - Se "exact" ou "above" → 100 pontos

    Returns:
        Float entre 0 e 100.
    """
    detail = seniority_result["detail"]

    if detail == "not_specified":
        return 70.0
    elif detail == "exact":
        return 100.0
    elif detail == "above":
        return 85.0
    elif detail == "below":
        return 50.0
    return 70.0


def calculate_score(match_result: dict) -> dict:
    """
    Calcula o score final com base no resultado do matcher.

    Args:
        match_result: Dicionário retornado por match_resume_to_job().

    Returns:
        Dicionário com score final e breakdown por categoria.
    """
    skills_score = score_skills(match_result["skills"])
    experience_score = score_experience(match_result["experience"])
    seniority_score = score_seniority(match_result["seniority"])

    final_score = (
        skills_score * WEIGHTS["skills"]
        + experience_score * WEIGHTS["experience"]
        + seniority_score * WEIGHTS["seniority"]
    )

    if final_score >= 90:
        label = "Excelente"
    elif final_score >= 75:
        label = "Muito bom"
    elif final_score >= 60:
        label = "Bom"
    else:
        label = "Precisa melhorar"

    return {
        "score": round(final_score, 2),
        "label": label,
        "breakdown": {
            "skills": round(skills_score, 2),
            "experience": round(experience_score, 2),
            "seniority": round(seniority_score, 2),
        },
    }
   