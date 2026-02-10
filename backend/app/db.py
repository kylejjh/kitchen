from pymongo import MongoClient

MONGO_URI = "mongodb://root:rootpassword@127.0.0.1:27017/?authSource=admin"

def ping_mongo() -> bool:
    client = MongoClient(MONGO_URI)
    try:
        client.admin.command("ping")
        return True
    finally:
        client.close()
