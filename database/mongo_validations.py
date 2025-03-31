from pymongo import MongoClient, errors
import os

def validate_connection() -> bool:
    try:
        uri = os.getenv("MONGO_URI")
        if not uri:
            print("❌ Error: La variable de entorno MONGO_URI no está definida.")
            return False
        
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)  # 5 seg timeout
        client.admin.command('ping')  # 👈 ping para forzar la conexión
        return True

    except errors.ConfigurationError as e:
        print("❌ URI mal formada:", e)
        return False

    except errors.OperationFailure as e:
        print("❌ Autenticación fallida:", e)
        return False

    except errors.ServerSelectionTimeoutError as e:
        print("❌ No se pudo conectar al cluster:", e)
        return False

    except Exception as e:
        print("❌ Error inesperado:", e)
        return False
