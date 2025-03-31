from telegram import Update
from telegram.ext import ContextTypes
from handlers.menu import get_main_menu
from services.openai_api import analyze_sentiment
from services.openai_api import user_conversations
from utils.decorators import log_user_interaction


async def capture_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text
    
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    user_conversations[user_id].append(f"Usuario: {message}")
    
@log_user_interaction
async def analyze_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_conversations or not user_conversations[user_id]:
        await update.callback_query.message.reply_text("Aún no tengo suficiente conversación para analizar. Chatea un poco más conmigo 🙂")
        return
    
    conversation_text = "\n".join(user_conversations[user_id])
    analysis = await analyze_sentiment(conversation_text)
    
    
    await update.message.reply_text(analysis)

    await update.message.reply_text(
        '¿En qué más puedo ayudarte?',
        reply_markup=get_main_menu()  
    )
 
    text = analysis + '¿En qué más puedo ayudarte?'
    return text, None
