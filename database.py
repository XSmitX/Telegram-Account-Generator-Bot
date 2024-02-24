import pymongo
from config import DB_URL

client = pymongo.MongoClient(DB_URL)
db = client["account_generator"]
collection = db["accounts"]
