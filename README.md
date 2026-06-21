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

## 🧪 Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/resume-analyzer.git
cd resume-analyzer
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv venv

# Windows (PowerShell com restrição de política)
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# Linux / macOS
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Instalar o modelo de linguagem do spaCy

```bash
.\venv\Scripts\python.exe -m spacy download pt_core_news_sm
```

### 4. Executar a API

```bash
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

---

## 🌐 Acessos

* API: http://127.0.0.1:8000
* Documentação: http://127.0.0.1:8000/docs

---


## 📌 Funcionalidades

- [x] Estrutura do projeto organizada
- [x] API base com FastAPI
- [x] Parser de currículo PDF (`core/parser.py`)
- [X] Extração de entidades com spaCy (`core/nlp.py`)
- [X] Comparação currículo × vaga (`core/matcher.py`)
- [X] Score de compatibilidade 0–100 (`core/scorer.py`)
- [X] Feedback inteligente com IA (`core/feedback.py`)
- [X] Interface web com Streamlit
---



## 👨‍💻 Autor

Gabriel Cavalcante
[LinkedIn](https://www.linkedin.com/in/gabrielcant/) · [GitHub](https://github.com/GabsCavalcant)
