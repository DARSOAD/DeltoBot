from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from services.weather_api import obtener_clima
from services.openai_api import obtener_recomendacion
from handlers.menu import start
from utils.decorators import log_user_interaction

# Estado de la conversación: recibir el nombre de la ciudad
CITY = 1


@log_user_interaction
async def start_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "¿En qué ciudad quieres saber el clima?"
    await update.message.reply_text(mensaje,reply_markup=ReplyKeyboardRemove())
    return mensaje, CITY 

@log_user_interaction
async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ciudad = update.message.text.strip()  # Obtener la ciudad enviada por el usuario

    # Realizar la llamada a la API de clima usando la ciudad ingresada
    response = obtener_clima(ciudad)

    if response.get("cod") != 200:
        mensaje = "No se encontró la ciudad. Por favor, inténtalo de nuevo."
        await update.message.reply_text(mensaje)
        return mensaje, CITY  # Volver al estado de esperar la ciudad

    # Obtener los detalles del clima y devolver una recomendación
    descripcion = response['weather'][0]['description']
    temperatura = response['main']['temp']
    recomendacion = await obtener_recomendacion(response,ciudad)

    # Enviar el mensaje con la información del clima y la recomendación
    mensaje = (f"El clima en {ciudad} es: {descripcion}\n"
               f"Temperatura: {temperatura}°C\n"
               f"Recomendación: {recomendacion}")

    await update.message.reply_text(mensaje)

     # Regresar al menú inicial después de dar la recomendación
    await start(update, context)  

    # Finalizar la conversación actual, pero continuar con el flujo del menú
    return mensaje, ConversationHandler.END

def weather_command():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^¡Quiero saber el clima! 🌞$"), start_weather)],
        states={
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
        },
        fallbacks=[],
        allow_reentry=True,         
        per_message=False 
    )