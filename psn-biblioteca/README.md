# PlayStation Library Manager | Backend API

Este projeto consiste em uma API RESTful para gerenciamento de bibliotecas de jogos PlayStation, desenvolvida como parte da avaliação de Backend do curso de **Engenharia de Software na Univassouras**. A aplicação utiliza uma arquitetura baseada em containers, garantindo portabilidade e isolamento do ambiente de banco de dados.

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 
* **Framework:** FastAPI (Alta performance e suporte nativo a operações assíncronas)
* **Banco de Dados:** MongoDB (NoSQL baseado em documentos)
* **Containerização:** Docker & Docker Compose
* **Validação de Dados:** Pydantic

## 📌 Funcionalidades (CRUD)

A API permite a manipulação completa do acervo de jogos com os seguintes atributos:
* `nome`: Título do jogo.
* `plataforma`: Console (PS4, PS5, etc.).
* `tipo_midia`: Físico ou Digital.
* `valor_pago`: Custo de aquisição.
\`\`\`

## 🚀 Como executar

\`\`\`bash
docker-compose up --build
\`\`\`

Acesse: http://localhost:8000