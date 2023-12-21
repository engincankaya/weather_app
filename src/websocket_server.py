import asyncio
import websockets
import json
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
PORT = os.getenv("PORT")


async def fetch_weather_data(client, city):
    """
    Belirli bir şehrin hava durumu verilerini alır ve günlük sıcaklıkları içeren listeyi döndürür.
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},TR&lang=tr&units=metric&appid={API_KEY}"

    response = await client.get(url)
    data = response.json()

    daily_temperatures = [
        entry for entry in data.get("list", []) if entry["dt_txt"].endswith("15:00:00")
    ]
    data["list"] = daily_temperatures
    return data


async def weather_info(websocket, path):
    """
    WebSocket üzerinden hava durumu bilgilerini belirli aralıklarla gönderir.
    """
    client = httpx.AsyncClient()

    try:
        while True:
            weather_info_list = []
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
                weather_data = await fetch_weather_data(client, city)
                weather_info_list.append(weather_data)

            await websocket.send(json.dumps(weather_info_list))

            await asyncio.sleep(30)

    finally:
        await client.aclose()


def start_websocket_server():
    """
    WebSocket sunucusunu başlatır ve belirtilen port üzerinden hava durumu bilgilerini gönderir.
    """
    asyncio.set_event_loop(asyncio.new_event_loop())

    start_server = websockets.serve(weather_info, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    start_websocket_server()
