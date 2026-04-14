from app.database.mongodb import mongodb

# Professor, exporto a instância do MongoDB pra usar nas rotas
# para deixar o importe mais limnpo

__all__ = ["mongodb"]