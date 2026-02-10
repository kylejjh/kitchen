from pymongo import MongoClient
from pymongo.database import Database

MONGO_URI = "mongodb://root:rootpassword@127.0.0.1:27017/?authSource=admin"
DB_NAME = "kitchen"

_client: MongoClient | None = None

def get_db() -> Database:
    """
    Return a MongoDB Database object.
    Uses a single MongoClient for the life of the process.
    """
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client[DB_NAME]

def ping_mongo() -> bool:
    # keep your existing behavior, but reuse the shared client if possible
    try:
        get_db().client.admin.command("ping")
        return True
    except Exception:
        return False
