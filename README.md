# 📊 Atlas Financeiro

O **Atlas Financeiro** é uma aplicação completa para gestão e controle de finanças pessoais e corporativas. O sistema permite o cadastro, categorização e acompanhamento em tempo real de receitas, despesas e relatórios consolidados.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python (FastAPI / Pydantic)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Banco de Dados:** SQLite / PostgreSQL (SQLAlchemy ORM)
- **Gerenciamento de Dependências:** Python Virtual Environment (`venv`)

---

## 📁 Estrutura do Projeto

```text
atlas-financeiro/
│
├── api/                  # Endpoints e versão da API
│   └── v1/
│       └── lancamentos/  # Regras de negócios e rotas
├── app/                  # Modelos, serviços e utilitários
│   ├── models/           # Mapeamento do banco de dados
│   ├── routers/          # Controladores das rotas
│   └── services/        # Lógica da aplicação
├── frontend/             # Interface do usuário
│   ├── css/              # Estilização visual
│   └── js/               # Scripts de interatividade
├── .gitignore            # Arquivos ignorados pelo Git
├── requirements.txt      # Dependências do projeto
└── main.py               # Ponto de entrada da aplicação