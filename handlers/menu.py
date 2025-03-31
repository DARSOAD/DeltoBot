from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("¡Quiero saber el clima! 🌞")],
        [KeyboardButton("¡Quiero contar! 🧊")],
        [KeyboardButton("¡Quiero analizar la conversación! 🧠")],
        [KeyboardButton("¡Adivina el clima! 🎮")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "¿En qué te puedo ayudar? 🫡",
        reply_markup=reply_markup
    )

def get_main_menu():
    keyboard = [
        [KeyboardButton("¡Quiero saber el clima! 🌞")],
        [KeyboardButton("¡Quiero contar! 🧊")],
        [KeyboardButton("¡Quiero analizar la conversación! 🧠")],
        [KeyboardButton("¡Adivina el clima! 🎮")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
