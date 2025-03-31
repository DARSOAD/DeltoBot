from functools import wraps
from services.openai_api import user_conversations
from telegram import Update
from telegram.ext import ContextTypes


"""
Este decorador permite que las funciones de handler retornen (mensaje:str, estado:int),
para registrar el mensaje del bot en la conversación del usuario.

Si se retorna solo un estado, no se guarda respuesta del bot.
"""
def log_user_interaction(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id

        # Mensaje del usuario
        if update.message and update.message.text:
            message = update.message.text
        elif update.callback_query and update.callback_query.data:
            message = update.callback_query.data
        else:
            message = "Entrada no reconocida"

        if user_id not in user_conversations:
            user_conversations[user_id] = []

        user_conversations[user_id].append(f"Usuario: {message}")

        # Ejecutamos el handler y esperamos una tupla (respuesta, estado) o solo estado
        result = await func(update, context, *args, **kwargs)

        # Si es una tupla (respuesta, estado), guardamos la respuesta
        if isinstance(result, tuple) and isinstance(result[0], str):
            user_conversations[user_id].append(f"Bot: {result[0]}")
            return result[1]
        
        return result

    return wrapper
