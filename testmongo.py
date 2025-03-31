# from pymongo import MongoClient
# import os
# from dotenv import load_dotenv
# load_dotenv()
# client = MongoClient(os.getenv("MONGO_URI"))
# db = client["delto_bot"]
# collection = db["user_counters"]
# print("Conexión exitosa a MongoDB Atlas ✅")
# print("🔎 URI cargada:", os.getenv("MONGO_URI"))
# result = collection.find_one_and_update(
#         {"user_id": 6300964970},
#         {"$inc": {"count": 1}},
#         upsert=True,
#         return_document=True
#     )

from database.mongo_validations import validate_connection

if validate_connection():
    print("✅ Conexión verificada con MongoDB Atlas")
else:
    print("🚫 No se pudo establecer conexión. Verificá tu .env")
    exit(1)