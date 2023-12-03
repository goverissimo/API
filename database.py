# database.py

from pymongo import MongoClient

def get_db():
    mongo_uri = "mongodb+srv://gscsverissimo:teste1234@cluster0.jrmrsy1.mongodb.net"
    client = MongoClient(mongo_uri)
    db = client['teste']
    return db

def wipe_database():
    db = get_db()
    collections = db.list_collection_names()
    # Delete each collection
    for collection in collections:
        db[collection].drop()

   



#wipe_database()
