# weather_api.py
import os
import requests
import random

WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

def obtener_clima(ciudad):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={WEATHER_API_KEY}&lang=es&units=metric'
    response = requests.get(url)
    return response.json()

CIUDADES_CONOCIDAS = [
    "Londres", "Nueva York", "París", "Tokio", "Madrid", "Roma", "Berlín", "Buenos Aires",
    "Ciudad de México", "São Paulo", "Lima", "Bogotá", "Toronto", "Los Ángeles", "Chicago",
    "Miami", "Estambul", "Sídney", "Seúl", "Bangkok", "Moscú", "Ámsterdam", "Lisboa", "Praga",
    "Viena", "Copenhague", "Oslo", "Estocolmo", "Helsinki", "Bruselas", "Zúrich", "Dublín",
    "Barcelona", "Milán", "Múnich", "Frankfurt", "Doha", "Dubái", "Riad", "Yakarta", "Manila",
    "Nueva Delhi", "Mumbai", "Shanghái", "Beijing", "Hong Kong", "Singapur", "Kuala Lumpur",
    "El Cairo", "Nairobi", "Casablanca", "Ciudad del Cabo", "Johannesburgo", "Caracas", 
    "Quito", "La Paz", "Asunción", "Montevideo", "Santiago", "San Juan", "Panamá", "San José",
    "Tegucigalpa", "Managua", "Guatemala", "San Salvador", "Kingston", "La Habana", "Doha",
    "Abu Dabi", "Bagdad", "Teherán", "Jerusalén", "Beirut", "Damasco", "Ankara", "Kiev", 
    "Varsovia", "Bucarest", "Sofía", "Belgrado", "Atenas", "Budapest", "Bratislava", "Tallin",
    "Riga", "Vilna", "Reikiavik", "Canberra", "Wellington", "Auckland", "Honolulu", "Anchorage",
    "Denver", "Houston", "Atlanta", "Seattle", "Boston", "Philadelphia", "Phoenix", "Detroit",
    "San Francisco", "Las Vegas", "San Diego", "Minneapolis", "Dallas", "Orlando", "Charlotte",
    "Pittsburgh", "Tampa", "Cleveland", "Cincinnati", "Indianápolis", "Kansas City", 
    "Salt Lake City", "Portland", "Baltimore", "St. Louis", "Milwaukee", "New Orleans",
    "Raleigh", "Richmond", "Albany", "Buffalo", "Columbus", "Toledo", "Des Moines", 
    "Omaha", "Fargo", "Boise", "Little Rock", "Birmingham", "Memphis", "Nashville", 
    "Louisville", "Tulsa", "Oklahoma City", "Albuquerque", "El Paso", "Honolulu"
]

def obtener_ciudad_temperatura():
    
    intentos = 0

    while intentos < 5:  # Intenta hasta 5 veces si la ciudad falla
        ciudad = random.choice(CIUDADES_CONOCIDAS)
        clima = obtener_clima(ciudad)

        if clima.get("cod") == 200:
            return ciudad, clima["main"]["temp"]

        intentos += 1

    # Si no se encontró ninguna ciudad válida tras 5 intentos:
    return None, None