from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
import time

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self._conectar()
    
    def _conectar(self):
        """Professor,  aqui  e o retry para coneção do NoSQL pro Docker
        """
        
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        
        #  aqui faz a tentativa e conexão
        for tentativa in range(1, 8):
            try:
                self.client = MongoClient(mongo_url, serverSelectionTimeoutMS=3000)
                self.client.admin.command('ping')
                self.db = self.client.psn_biblioteca
                print(f"🎮 Conectado ao MongoDB na tentativa {tentativa}!")
                return
            except ServerSelectionTimeoutError:
                if tentativa == 7:
                    raise Exception("❌ MongoDB não respondeu. Verifique se o container tá rodando")
                print(f"⏳ Aguardando MongoDB iniciar... ({tentativa}/7)")
                time.sleep(3)
    
    def get_collection(self):
        return self.db.jogos

mongodb = MongoDB()