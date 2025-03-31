from telegram import Update
from telegram.ext import ContextTypes
from database.mongo import increment_user_count
from handlers.menu import get_main_menu
from utils.decorators import log_user_interaction

@log_user_interaction
async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    new_count = increment_user_count(user_id)

    if new_count == 0:
        text = "No hemos encontrado tu cuenta en la base de datos. ¿Podrías intentar de nuevo?"
    else:
        text = f"Has contado {new_count} veces. ¡Sigue contando!"

    await update.message.reply_text(
        text,
        reply_markup=get_main_menu()  
    )

    return text, None

    

