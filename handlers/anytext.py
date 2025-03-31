from telegram import Update
from telegram.ext import ContextTypes
from handlers.menu import get_main_menu
from services.openai_api import anytext_handler_opneAI, user_conversations
from utils.decorators import log_user_interaction

@log_user_interaction
async def anytext_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    conversation_text = "\n".join(user_conversations[user_id])
    respuesta = await anytext_handler_opneAI(conversation_text)

    await update.message.reply_text(respuesta, reply_markup=get_main_menu())

    return respuesta, None
