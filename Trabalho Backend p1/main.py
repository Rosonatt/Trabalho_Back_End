from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = FastAPI(title="Trabalho de Backend")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client.robotica_db
colecao = db.componentes

class Componente(BaseModel):
    nome_peca: str
    compatibilidade: str
    projeto_alvo: str
    quantidade_estoque: int

@app.get("/", response_class=HTMLResponse)
def interface_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inventário - TimeNataliaeRosonatt</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; color: #333; }
            .container { max-width: 900px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            h1, h2 { color: #2c3e50; text-align: center; margin-bottom: 5px;}
            .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; font-size: 0.9em; }
            .form-group { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
            input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; min-width: 150px; }
            button { padding: 10px 20px; background-color: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
            button:hover { background-color: #2ecc71; }
            .btn-delete { background-color: #e74c3c; padding: 5px 10px; font-size: 0.8em; }
            .btn-delete:hover { background-color: #c0392b; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }
            th { background-color: #34495e; color: white; }
            tr:hover { background-color: #f1f1f1; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Gestão de Componentes Robóticos</h1>
            <div class="subtitle">Desenvolvido por Natalia e Rosonatt | Riuassa</div>
            
            <h2>Adicionar Novo Componente</h2>
            <form id="crudForm" class="form-group">
                <input type="text" id="nome" placeholder="Nome da Peça" required>
                <input type="text" id="compat" placeholder="Compatibilidade (ex: ESP32)" required>
                <input type="text" id="projeto" placeholder="Projeto Alvo (ex: HÍGIA)" required>
                <input type="number" id="estoque" placeholder="Qtd em Estoque" required>
                <button type="submit">Salvar</button>
            </form>

            <h2>Lista de Componentes</h2>
            <table>
                <thead>
                    <tr>
                        <th>Nome da Peça</th>
                        <th>Compatibilidade</th>
                        <th>Projeto Alvo</th>
                        <th>Estoque</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody id="tabelaCorpo">
                    <!-- Os itens vão aparecer aqui -->
                </tbody>
            </table>
        </div>

        <script>
            // Função para carregar os dados da API e montar a tabela
            async function carregarDados() {
                const response = await fetch('/componentes/');
                const data = await response.json();
                const tbody = document.getElementById('tabelaCorpo');
                tbody.innerHTML = '';
                
                data.forEach(item => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${item.nome_peca}</td>
                        <td>${item.compatibilidade}</td>
                        <td>${item.projeto_alvo}</td>
                        <td>${item.quantidade_estoque}</td>
                        <td>
                            <button class="btn-delete" onclick="deletarItem('${item._id}')">Deletar</button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            }

            // Função para salvar um novo item
            document.getElementById('crudForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const novoItem = {
                    nome_peca: document.getElementById('nome').value,
                    compatibilidade: document.getElementById('compat').value,
                    projeto_alvo: document.getElementById('projeto').value,
                    quantidade_estoque: parseInt(document.getElementById('estoque').value)
                };

                await fetch('/componentes/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(novoItem)
                });

                document.getElementById('crudForm').reset();
                carregarDados(); // Recarrega a tabela
            });

            // Função para deletar um item
            async function deletarItem(id) {
                if(confirm('Tem certeza que deseja deletar?')) {
                    await fetch(`/componentes/${id}`, { method: 'DELETE' });
                    carregarDados(); // Recarrega a tabela
                }
            }

            // Carrega a tabela assim que a página abre
            carregarDados();
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/componentes/")
def criar_componente(comp: Componente):
    resultado = colecao.insert_one(comp.model_dump())
    return {"mensagem": "Criado com sucesso", "id": str(resultado.inserted_id)}

@app.get("/componentes/")
def listar_tudo():
    lista = []
    for item in colecao.find():
        item["_id"] = str(item["_id"]) 
        lista.append(item)
    return lista

@app.get("/componentes/{id}")
def buscar_um(id: str):
    item = colecao.find_one({"_id": ObjectId(id)})
    if item:
        item["_id"] = str(item["_id"])
        return item
    return {"erro": "Componente não encontrado"}

@app.put("/componentes/{id}")
def atualizar_componente(id: str, comp: Componente):
    resultado = colecao.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": comp.model_dump()}
    )
    if resultado.modified_count == 1:
        return {"mensagem": "Atualizado com sucesso"}
    return {"erro": "Componente não encontrado ou dados são os mesmos"}

@app.delete("/componentes/{id}")
def deletar_componente(id: str):
    resultado = colecao.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 1:
        return {"mensagem": "Deletado com sucesso"}
    return {"erro": "Componente não encontrado para deletar"}