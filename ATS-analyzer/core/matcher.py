# core/matcher.py

"""
Módulo de comparação entre currículo e vaga.

Responsabilidade: receber dois perfis estruturados (saída do nlp.py)
e calcular a compatibilidade entre eles.

Não sabe nada sobre PDFs, não sabe nada sobre scores finais.
Só compara e retorna os dados brutos da comparação.
"""

from core.nlp import analyze_text


# ---------------------------------------------------------------------------
# Funções de comparação
# ---------------------------------------------------------------------------

def match_skills(resume_skills: list, job_skills: list) -> dict:
    """
    Compara as skills do currículo com as skills da vaga.

    Usamos sets (conjuntos) porque:
    - Eliminam duplicatas automaticamente
    - Operações de interseção e diferença são nativas e eficientes
    - É exatamente o que a similaridade de Jaccard precisa

    Args:
        resume_skills: Lista de skills do currículo.
        job_skills: Lista de skills da vaga.

    Returns:
        Dict com matched, missing, extra e o match_rate (0.0 a 1.0).
    """
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = resume_set & job_set        # interseção: tem nos dois
    missing = job_set - resume_set        # vaga pede, currículo não tem
    extra = resume_set - job_set          # currículo tem, vaga não pede
    union = resume_set | job_set          # união: tudo junto

    # Jaccard similarity — evita divisão por zero se ambas as listas forem vazias
    match_rate = len(matched) / len(union) if union else 0.0

    return {
        "matched": sorted(matched),      # sorted() só pra ficar organizado na exibição
        "missing": sorted(missing),
        "extra": sorted(extra),
        "match_rate": round(match_rate, 2),
    }


def match_seniority(resume_seniority: str, job_seniority: str) -> dict:
    """
    Compara o nível de senioridade do candidato com o exigido pela vaga.

    Usamos um mapa numérico pra comparar níveis ordinais.
    'junior' < 'mid' < 'senior' — isso não é possível comparar com strings puras.

    Returns:
        Dict com is_match (bool) e gap (diferença numérica entre os níveis).
        gap positivo = candidato acima do exigido (ok)
        gap negativo = candidato abaixo do exigido (problema)
        gap zero     = match perfeito
    """
    level_map = {
        "junior": 1,
        "mid": 2,
        "senior": 3,
        "not_specified": None,
    }

    resume_level = level_map.get(resume_seniority)
    job_level = level_map.get(job_seniority)

    # Se qualquer um não foi especificado, não penalizamos nem bonificamos
    if resume_level is None or job_level is None:
        return {"is_match": True, "gap": 0, "detail": "not_specified"}

    gap = resume_level - job_level

    return {
        "is_match": gap >= 0,   # candidato no nível certo ou acima = ok
        "gap": gap,
        "detail": "above" if gap > 0 else "exact" if gap == 0 else "below",
    }


def match_experience(resume_years: int | None, job_years: int | None) -> dict:
    """
    Compara anos de experiência do candidato com o mínimo exigido.

    Returns:
        Dict com is_match e gap em anos.
        gap positivo = candidato tem mais experiência que o exigido
        gap negativo = candidato tem menos experiência que o exigido
    """
    # Se algum dos dois não foi especificado, não penalizamos
    if resume_years is None or job_years is None:
        return {"is_match": True, "gap": None, "detail": "not_specified"}

    gap = resume_years - job_years

    return {
        "is_match": gap >= 0,
        "gap": gap,
        "detail": f"{resume_years} anos (exigido: {job_years})",
    }


# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------

def match_resume_to_job(resume_text: str, job_text: str) -> dict:
    """
    Função principal. Recebe os dois textos, analisa ambos e compara.

    Fluxo:
    texto currículo → nlp → perfil currículo ↘
                                               matcher → resultado
    texto vaga      → nlp → perfil vaga      ↗

    Args:
        resume_text: Texto limpo do currículo.
        job_text: Texto da descrição da vaga.

    Returns:
        Dicionário completo com todos os resultados da comparação.
    """
    resume_profile = analyze_text(resume_text)
    job_profile = analyze_text(job_text)

    skills_result = match_skills(
        resume_profile["skills"],
        job_profile["skills"],
    )

    seniority_result = match_seniority(
        resume_profile["seniority"],
        job_profile["seniority"],
    )

    experience_result = match_experience(
        resume_profile["years_experience"],
        job_profile["years_experience"],
    )

    return {
        "skills": skills_result,
        "seniority": seniority_result,
        "experience": experience_result,
        "resume_profile": resume_profile,
        "job_profile": job_profile,
    }