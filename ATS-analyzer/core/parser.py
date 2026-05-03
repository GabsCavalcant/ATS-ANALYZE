# core/parser.py

"""
Parser de currículos em PDF.

Responsabilidade: receber um arquivo PDF e retornar o texto limpo como string.
Nada mais, nada menos. Outras camadas cuidam do que fazer com esse texto.
"""

import pdfplumber
import re
from pathlib import Path


def extract_text_from_pdf(file_path: str) -> str:
    """
    Abre o PDF e extrai o texto bruto de todas as páginas.

    Por que iterar página por página?
    - PDFs são documentos paginados. pdfplumber expõe cada página separadamente.
    - Alguns PDFs têm textos diferentes por página (ex: currículo de 2 páginas).
    - Concatenamos tudo com '\n' para preservar quebras entre páginas.

    Args:
        file_path: Caminho para o arquivo PDF (string ou Path).

    Returns:
        Texto bruto extraído, sem limpeza.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o PDF não tiver texto extraível (ex: PDF escaneado como imagem).
    """
    path = Path(file_path)  # Path() normaliza o caminho em qualquer OS

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Formato inválido. Esperado: .pdf | Recebido: {path.suffix}")

    raw_pages = []

    with pdfplumber.open(path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            if text:  # Página pode retornar None se for imagem
                raw_pages.append(text)
            else:
                # Avisa mas não quebra — o currículo pode ter páginas mistas
                print(f"[parser] Aviso: página {page_number} sem texto extraível.")

    if not raw_pages:
        raise ValueError(
            "Nenhum texto foi extraído. O PDF pode ser baseado em imagem (escaneado). "
            "Futuramente, OCR será necessário para esse caso."
        )

    return "\n".join(raw_pages)


def clean_text(raw_text: str) -> str:
    """
    Limpa o texto extraído do PDF.

    PDFs frequentemente geram lixo na extração:
    - Espaços múltiplos entre palavras
    - Linhas em branco excessivas
    - Caracteres de controle invisíveis

    Por que não fazer tudo em uma regex só?
    - Clareza. Cada linha tem um propósito legível.
    - Facilidade de manutenção e debug.

    Args:
        raw_text: Texto bruto vindo do PDF.

    Returns:
        Texto limpo, pronto para análise.
    """
    # 1. Remove caracteres de controle (exceto \n que queremos preservar)
    text = re.sub(r'[^\S\n]+', ' ', raw_text)
    # Explicação do regex:
    # [^\S\n]  → qualquer whitespace que NÃO seja \n (pega tab, espaço, \r, etc.)
    # +        → uma ou mais ocorrências
    # ' '      → substitui por espaço simples

    # 2. Remove espaços no início e fim de cada linha
    lines = [line.strip() for line in text.splitlines()]

    # 3. Remove linhas completamente vazias consecutivas (mantém no máximo 1)
    cleaned_lines = []
    previous_was_empty = False

    for line in lines:
        is_empty = (line == "")

        if is_empty and previous_was_empty:
            continue  # Pula linhas vazias consecutivas

        cleaned_lines.append(line)
        previous_was_empty = is_empty

    # 4. Junta tudo de volta e remove espaços nas bordas do texto inteiro
    return "\n".join(cleaned_lines).strip()


def parse_resume(file_path: str) -> dict:
    """
    Função principal do parser. Orquestra extração e limpeza.

    Por que retornar dict em vez de string pura?
    - Flexibilidade: futuramente podemos adicionar metadados (nº de páginas,
      nome do arquivo, data de parse, etc.) sem quebrar quem usa essa função.
    - É um padrão comum em APIs e sistemas profissionais.

    Args:
        file_path: Caminho para o arquivo PDF.

    Returns:
        Dicionário com:
        - 'text': texto limpo do currículo
        - 'source': nome do arquivo
        - 'status': 'success' ou 'error'
        - 'message': detalhes em caso de erro
    """
    try:
        raw_text = extract_text_from_pdf(file_path)
        clean = clean_text(raw_text)

        return {
            "text": clean,
            "source": Path(file_path).name,
            "status": "success",
            "message": None,
        }

    except (FileNotFoundError, ValueError) as e:
        # Erros esperados: arquivo não existe, PDF inválido, etc.
        return {
            "text": "",
            "source": Path(file_path).name,
            "status": "error",
            "message": str(e),
        }