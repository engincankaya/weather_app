import asyncio
import websockets
import json
from aiohttp import ClientSession
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
PORT = os.getenv("PORT")


async def fetch_weather_data(session, city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},TR&lang=tr&units=metric&appid={API_KEY}"
    async with session.get(url) as response:
        data = await response.json()

        daily_temperatures = [
            entry
            for entry in data.get("list", [])
            if entry["dt_txt"].endswith("15:00:00")
        ]
        data["list"] = daily_temperatures
        return data


async def weather_info(websocket, path):
    async with ClientSession() as session:
        while True:
            weather_info_list = []
            cities = [
                "Adana",
                "Adiyaman",
                "Afyonkarahisar",
                "Agri",
                "Ankara",
                "Antalya",
                "Duzce",
                "Edirne",
                "Istanbul",
                "Izmir",
            ]

            for city in cities:
                weather_data = await fetch_weather_data(session, city)
                weather_info_list.append(weather_data)

            await websocket.send(json.dumps(weather_info_list))

            await asyncio.sleep(30)


def start_websocket_server():
    asyncio.set_event_loop(asyncio.new_event_loop())

    start_server = websockets.serve(weather_info, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    start_websocket_server()
