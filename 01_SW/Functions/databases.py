
from pymongo import MongoClient

class MongoDB:
  def connect_to_mongodb(self):
    """Connexion à MongoDB"""
    try:
        self.uri = "mongodb://localhost:27017/"
        self.client = MongoClient(self.uri)
        self.db = self.client.app
        self.collection = self.db.test_job
        self.historique = self.db.historique
        return self.uri , self.client , self.db , self.collection , self.historique
    except Exception:
        self.client=None


class Mysql:
  pass