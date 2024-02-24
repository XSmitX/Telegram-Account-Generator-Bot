import pymongo
from config import MongoDB_Atalas_COnnection_String

client = pymongo.MongoClient(MongoDB_Atalas_COnnection_String)
db = client["account_generator"]
collection = db["accounts"]
