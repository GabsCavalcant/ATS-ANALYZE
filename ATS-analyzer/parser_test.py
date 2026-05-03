# test_parser.py
from core.parser import parse_resume

result = parse_resume("curriculo.pdf")  # coloca o nome do seu PDF aqui

if result["status"] == "success":
    print(f"✅ Arquivo: {result['source']}")
    print(f"\n📄 Primeiros 500 caracteres:\n")
    print(result["text"][:500])
else:
    print(f"❌ Erro: {result['message']}")