from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from database.mongo import increment_weather_game_score
from services.weather_api import obtener_ciudad_temperatura
from handlers.menu import start
from utils.decorators import log_user_interaction
from services.openai_api import user_conversations

# Estado de la conversación: recibir la temperatura
TEMP = 1
temperaturaBot = 0
temperaturaUsuario = 0

@log_user_interaction
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje =  """
    ✨ Bienvenido al juego "Adivina el Clima" 🌍🌡️

    **Objetivo:**
    Tu misión es adivinar la temperatura actual en diferentes ciudades del mundo. El bot te enviará una ciudad aleatoria y tú tendrás que adivinar la temperatura en esa ciudad.

    **¿Cómo jugar?**
    1. El bot te dará el nombre de una ciudad al azar.
    2. Tienes que adivinar la temperatura en esa ciudad.
    3. El puntaje depende de cuán cerca estés de la temperatura real:
        - ¡Si adivinas la temperatura exacta, obtienes 100 puntos!
        - ¡Si estás cerca, pero no exactamente, todavía puedes ganar hasta 75 puntos!
        - Si estás un poco lejos, aún puedes obtener algunos puntos (**50 puntos**).
        - Y si fallas mucho, no te preocupes, ¡todavía obtienes 10 puntos!

    ¡Vamos a comenzar! ¿Cuál es la temperatura en la ciudad que te voy a dar?
    """
    await update.message.reply_text(mensaje)
    ciudad, temperaturaBot = obtener_ciudad_temperatura()    # Obtener la ciudad y la temperatura del bot
    if ciudad is None:
        await update.message.reply_text("Tengo un pequeño problema con el juego, Intenta de nuevo más tarde.")
        return ConversationHandler.END
    
    context.user_data["temperaturaBot"] = temperaturaBot  # Guardar la temperatura del bot en el contexto del usuario
    await update.message.reply_text(f"¿Cuál es la temperatura en {ciudad}?")
    await update.message.reply_text("Escribe la temperatura en grados Celsius (°C)",reply_markup=ReplyKeyboardRemove())
    return mensaje, TEMP

async def get_temp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temperaturaUsuario = update.message.text.strip()  # Obtener la ciudad enviada por el usuario

    try:
        temperaturaUsuario = float(temperaturaUsuario)  # ✅ Conversión segura
    except ValueError:
        await update.message.reply_text("Por favor, ingresa un número válido (por ejemplo: 22 o 22.5)")
        return "Entrada inválida", TEMP

    temperaturaBot = context.user_data.get("temperaturaBot", None)
    if temperaturaBot is None:
        await update.message.reply_text("Ocurrió un error interno. Vuelve a iniciar el juego.")
        return "Error en juego", ConversationHandler.END
    
    diferencia = abs(temperaturaUsuario - temperaturaBot)  # Calcular la diferencia entre la temperatura del usuario y la del bot

    puntaje = 0
    if diferencia == 0:
        puntaje = 100  # Adivinanza exacta
    elif diferencia <= 5:
        puntaje = 75  # Cerca
    elif diferencia <= 10:
        puntaje = 50  # Moderadamente cerca
    else:
        puntaje = 10  # Muy lejos

    #Inserción de puntaje en la base de datos

    user_id = update.message.from_user.id
    new_count = increment_weather_game_score(user_id, puntaje)  # Incrementar el puntaje del usuario en la base de datos

    if new_count == 0:
        text = "No hemos encontrado tu cuenta en la base de datos. ¿Podrías intentar de nuevo?"
    else:
        text = f"Tu nuevo puntaje es: {new_count}. ¡Compartelo con tus amigos! ¿Quién es el mejor jugador?"


    # # Enviar el mensaje con la información del clima y la recomendación
    mensaje = ( f"La temperatura actual era: {temperaturaBot}°C\n Obtienes {puntaje} puntos!. \n {text}.\n")

    await update.message.reply_text(mensaje)

    # Regresar al menú inicial después de dar la recomendación
    await start(update, context)  

    user_conversations[user_id].append(f"Bot: {mensaje}")

    return ConversationHandler.END

def game_weather_command():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^¡Adivina el clima! 🎮$"), start_game)],
        states={
            TEMP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_temp)],
        },
        fallbacks=[],
        allow_reentry=True,         
        per_message=False          
    ) 