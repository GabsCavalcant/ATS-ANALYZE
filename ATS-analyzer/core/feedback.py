# core/feedback.py

"""
Módulo de feedback inteligente.

Responsabilidade: receber o resultado do scorer e gerar
feedback humanizado usando IA (Groq).
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def _configure_groq():
    """
    Configura o cliente Groq com a key do .env.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY não encontrada. "
            "Verifique se o arquivo .env existe e contém a chave."
        )

    return Groq(api_key=api_key)


def _build_prompt(score_result: dict, match_result: dict) -> str:
    """
    Monta o prompt enviado para a IA.
    """
    score      = score_result["score"]
    label      = score_result["label"]
    breakdown  = score_result["breakdown"]
    matched    = match_result["skills"]["matched"]
    missing    = match_result["skills"]["missing"]
    extra      = match_result["skills"]["extra"]
    experience = match_result["experience"]["detail"]
    seniority  = match_result["seniority"]["detail"]

    return f"""
Você é um especialista em recrutamento e desenvolvimento de carreira.
Analise os dados abaixo e gere um feedback profissional e construtivo em português.

## Dados da análise

- Score geral: {score}/100 ({label})
- Score de skills: {breakdown['skills']}/100
- Score de experiência: {breakdown['experience']}/100
- Score de senioridade: {breakdown['seniority']}/100

- Skills que batem com a vaga: {', '.join(matched) if matched else 'nenhuma'}
- Skills que estão faltando: {', '.join(missing) if missing else 'nenhuma'}
- Skills extras do candidato: {', '.join(extra) if extra else 'nenhuma'}

- Experiência: {experience}
- Senioridade: {seniority}

## Instruções

Gere um feedback com exatamente 3 seções:

1. **Pontos fortes** (2-3 frases sobre o que o candidato tem de bom)
2. **Pontos de melhoria** (2-3 frases sobre o que falta, com sugestões práticas)
3. **Recomendação final** (1-2 frases diretas sobre as chances nessa vaga)

Seja direto, honesto e construtivo. Mencione as skills específicas dos dados.
""".strip()


def generate_feedback(score_result: dict, match_result: dict) -> dict:
    """
    Função principal. Gera feedback inteligente com o Groq.

    Args:
        score_result: Retorno do calculate_score() do scorer.py
        match_result: Retorno do match_resume_to_job() do matcher.py

    Returns:
        Dicionário com o feedback gerado e metadados.
    """
    try:
        client = _configure_groq()
        prompt = _build_prompt(score_result, match_result)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # modelo gratuito do Groq
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return {
            "status": "success",
            "feedback": response.choices[0].message.content,
            "score": score_result["score"],
            "label": score_result["label"],
        }

    except ValueError as e:
        return {"status": "error", "message": str(e)}

    except Exception as e:
        return {"status": "error", "message": f"Erro ao chamar a API: {str(e)}"}