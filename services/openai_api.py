import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

user_conversations = {}

async def obtener_recomendacion(response,ciudad):
    # Obtener la descripción del clima
    descripcion = response['weather'][0]['description']
    # Construir el prompt con la descripción del clima
    prompInstructions = f"El clima es: {descripcion}. y la ciudad en la que estamos es {ciudad}."	
    prompInput = f"Da 5 recomendaciones para una persona en esta condición climática y 5 lugares turísticos para ir en esas condiciones climáticas en esa {ciudad}."

    try:
        # Llamar a la API de OpenAI para obtener una recomendación
        completion = client.responses.create(
            model="gpt-4o", 
            instructions=prompInstructions,
            input=prompInput
        )
        
        # Obtener la recomendación de la respuesta
        recomendacion = completion.output_text
        return recomendacion
    
    except Exception as e:
        print(f"Error al obtener recomendación de OpenAI: {e}")
        return "No se pudo obtener una recomendación en este momento."

async def analyze_sentiment(conversation: str) -> str:
    prompInstructions = f"Analiza el sentimiento de la siguiente conversación entre un usuario y un bot. "	
    prompInput = f"Clasifica como positiva, negativa o neutral, y da una breve explicación de la siguiente conversación: {conversation}."

    # print(conversation)

    try:
        # Llamar a la API de OpenAI para obtener un análisis de sentimiento
        completion = client.responses.create(
            model="gpt-4o", 
            instructions=prompInstructions,
            input=prompInput
        )
        
        # Obtener el análisis de la respuesta
        analisis = completion.output_text
        return analisis
    
    except Exception as e:
        print(f"Error al obtener el análisis de OpenAI: {e}")
        return "No se pudo obtener un análisis en este momento."
    
async def anytext_handler_opneAI(conversation: str) -> str:
    prompInstructions =f"""Vas a recibir una conversación entre un usuario y un bot. El bot está diseñado únicamente para:

                            1. Hacer recomendaciones de lugares turísticos

                            2. Brindar información sobre el clima

                            3. Hacer conteos simples (por ejemplo, cuántos lugares hay en una lista)

                            4. Analizar el sentimiento de la conversación

                            5. Jugar un juego de adivinanza sobre el clima

                            Analiza la conversación y genera una respuesta que el bot podría dar si el usuario hace una pregunta o solicitud que está fuera del alcance de estas funciones.

                            La respuesta del bot debe:

                            Ser muy amigable con un lenguaje sencillo y con confianza

                            Mantener el tono amable y útil

                            Disculparse con el usuario por no poder cumplir con su solicitud

                            Redirigir de manera natural y fluida hacia el uso del menú usando este emoji 👇, indicando que es la forma más eficiente de interactuar con el bot
                            
                            Si lo que escribe el usuario esta dentro de las funciones del bot, indicale que debe seleccionar una opción del menú para que el bot pueda ayudarle."

                            La salida debe ser solo el texto plano del bot, sin explicaciones ni etiquetas adicionales."""	
    prompInput = f"Esta es la conversación: {conversation}."

    # print(conversation)
    
    try:
        # Llamar a la API de OpenAI para obtener un análisis de sentimiento
        completion = client.responses.create(
            model="gpt-4o", 
            instructions=prompInstructions,
            input=prompInput
        )
        
        # Obtener el análisis de la respuesta
        analisis = completion.output_text
        return analisis
    
    except Exception as e:
        print(f"Error al obtener el análisis de OpenAI: {e}")
        return "No se pudo obtener un análisis en este momento."