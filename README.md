# 🧠 ATS Analyzer (AI Resume Analyzer)

Sistema inteligente que simula um **ATS (Applicant Tracking System)** para análise de currículos com base em descrições de vagas.

## 🚀 Objetivo

Este projeto tem como objetivo avaliar a compatibilidade entre um currículo e uma vaga, utilizando técnicas de **Processamento de Linguagem Natural (NLP)** e **Inteligência Artificial**.

---

## ⚙️ Tecnologias Utilizadas

* Python
* FastAPI
* Streamlit (futuro frontend)
* scikit-learn
* spaCy
* pdfplumber

---

## 🏗️ Estrutura do Projeto

```bash
resume-analyzer/
│
├── app/
│   └── main.py
│
├── core/
│   ├── parser.py
│   ├── nlp.py
│   ├── matcher.py
│   ├── scorer.py
│   └── feedback.py
│
├── frontend/
├── models/
├── utils/
│
├── requirements.txt
└── README.md
```

---

## 🧪 Como Executar o Projeto

### 1. Criar ambiente virtual

```bash
python -m venv venv
```

### 2. Instalar dependências

```bash
pip install fastapi uvicorn streamlit scikit-learn spacy pdfplumber
```

### 3. Executar a API

```bash
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

---

## 🌐 Acessos

* API: http://127.0.0.1:8000
* Documentação: http://127.0.0.1:8000/docs

---

## 📌 Funcionalidades (em desenvolvimento)

* Upload de currículo (PDF)
* Extração de texto
* Análise de palavras-chave
* Cálculo de score de compatibilidade
* Feedback inteligente com IA

---

## 📈 Próximos Passos

* Implementar parser de currículo
* Adicionar similaridade semântica (embeddings)
* Criar interface com Streamlit
* Gerar sugestões automáticas de melhoria

---

## 👨‍💻 Autor

Gabriel Cavalcante
