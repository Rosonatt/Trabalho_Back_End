# 🎮 Biblioteca PlayStation - CRUD FastAPI + MongoDB

## ✅ Requisitos Atendidos

- **Backend CRUD**: Todas as operações implementadas (Create, Read, Update, Delete)
- **FastAPI**: Framework utilizado para construir a API REST
- **MongoDB**: Banco de dados NoSQL para persistência
- **Docker**: Aplicação e banco rodando em containers separados
- **4 Atributos**: nome, plataforma, tipo_midia, valor_pago
- **Tema**: Biblioteca de jogos PlayStation (NÃO é usuários nem produtos)

## 📦 Estrutura

\`\`\`
app/
├── models/jogo.py       # Schema com 4 atributos principais
├── database/mongodb.py  # Conexão com MongoDB
├── main.py              # Rotas CRUD completas
└── static/index.html    # Interface web

Dockerfile               # Container da API
docker-compose.yml       # Orquestra API + MongoDB
\`\`\`

## 🚀 Como executar

\`\`\`bash
docker-compose up --build
\`\`\`

Acesse: http://localhost:8000