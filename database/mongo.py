from pymongo import MongoClient
import os
from database.mongo_validations import validate_connection


client = MongoClient(os.getenv("MONGO_URI"))
db = client["delto_bot"]
collection = db["user_counters"]

def get_user_count(user_id: int) -> int:
    user = collection.find_one({"user_id": user_id})
    return user["count"] if user else 0

def increment_user_count(user_id: int) -> int:

    if validate_connection():
        print("✅ Conexión verificada con MongoDB Atlas")
    else:
        print("🚫 No se pudo establecer conexión. Verificá tu .env")
        return 0
    result = collection.find_one_and_update(
        {"user_id": user_id},
        {"$inc": {"count": 1}},
        upsert=True,
        return_document=True
    )

    return result["count"]

def increment_weather_game_score(user_id: int, score: int) -> int:

    if not validate_connection():
        print("🚫 No se pudo establecer conexión. Verificá tu .env")
        return 0

    print("✅ Conexión verificada con MongoDB Atlas")

    result = collection.find_one_and_update(
        {"user_id": user_id},
        {"$inc": {"game_score": score}},  # ✅ Incrementa según el score entregado
        upsert=True,
        return_document=True  # Para retornar el documento actualizado
    )

    return result.get("game_score", 0)  # ✅ Retorna el nuevo puntaje actualizado