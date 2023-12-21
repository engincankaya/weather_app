import asyncio
import websockets
import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
PORT = os.getenv("PORT")


async def fetch_weather_data(city):
    """
    Belirli bir şehrin hava durumu verilerini alır.

    Args:
        city (str): Hava durumu bilgilerinin alınacağı şehir.

    Returns:
        dict: Şehrin hava durumu verilerini içeren sözlük.
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},TR&lang=tr&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    daily_temperatures = list()
    if data["list"] is not None:
        for entry in data["list"]:
            date_time = entry["dt_txt"]
            if date_time.endswith("15:00:00"):
                daily_temperatures.append(entry)
        data["list"] = daily_temperatures
        return data


async def weather_info(websocket, path):
    """
    WebSocket üzerinden sürekli olarak hava durumu bilgilerini gönderir.

    Args:
        websocket (WebSocket): Bilgilerin gönderileceği WebSocket nesnesi.
        path: WebSocket'in bağlandığı yol (kullanılmıyor).
    """
    while True:
        weather_info_list = list()
        cities = [
            "Adana",
            "Adiyaman",
            "Afyonkarahisar",
            "Agri",
            "Ankara",
            "Antalya",
            "Ardahan",
            "Artvin",
            "Aydin",
            "Bayburt",
            "Bursa",
            "Canakkale",
            "Diyarbakir",
            "Duzce",
            "Edirne",
            "Istanbul",
            "Izmir",
        ]

        for city in cities:
            weather_data = await fetch_weather_data(city)
            if weather_data:
                weather_info_list.append(weather_data)

        await websocket.send(json.dumps(weather_info_list))

        time.sleep(30)


def start_websocket_server():
    """
    WebSocket sunucusunu başlatır ve sürekli olarak hava durumu bilgilerini gönderir.
    """
    # Yeni bir etkinlik döngüsü oluştur
    asyncio.set_event_loop(asyncio.new_event_loop())

    start_server = websockets.serve(weather_info, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    start_websocket_server()
