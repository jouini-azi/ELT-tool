
from pymongo import MongoClient

class MongoDB:
  def init_mongo(self):
    """Connexion à MongoDB"""
    try:
        self.uri = "mongodb://localhost:27017/"
        self.client = MongoClient(self.uri)
        self.db = self.client.app
        self.collection = self.db.test_job
        self.hist = self.db.historique
    except Exception:
        self.client=None