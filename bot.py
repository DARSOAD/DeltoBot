from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler,MessageHandler, filters
from handlers.menu import start
from handlers.weather import weather_command
from handlers.counter import count_command
from handlers.sentiment import analyze_conversation
from handlers.anytext import anytext_handler
from handlers.game_weather import game_weather_command
import os

load_dotenv()



TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


async def clear_bot_commands(app):
    await app.bot.delete_my_commands() 


def main():
    # Inicialización el bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.post_init = clear_bot_commands
    
    app.add_handler(CommandHandler("start", start))

    # Handlers
    app.add_handler(weather_command())
    app.add_handler(MessageHandler(filters.Regex("^¡Quiero contar! 🧊$"), count_command))
    app.add_handler(MessageHandler(filters.Regex("^¡Quiero analizar la conversación! 🧠$"), analyze_conversation))
    app.add_handler(game_weather_command())

    # Catch-all handler para cualquier texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anytext_handler))
    

    # Bot con polling
    app.run_polling()

if __name__ == '__main__':
    main()
