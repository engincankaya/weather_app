import asyncio
import websockets
import requests
import json
import time


async def hava_durumu_api_cek(sehir):
    API_KEY = "7fdb6f5734ab0e721e58db2859bffe7c"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={sehir},TR&lang=tr&units=metric&appid={API_KEY}"
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


async def hava_durumu(websocket, path):
    while True:
        hava_durumu_bilgisi_list = list()
        sehirler = [
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

        for sehir in sehirler:
            hava_durumu_bilgisi = await hava_durumu_api_cek(sehir)
            if hava_durumu_bilgisi:
                hava_durumu_bilgisi_list.append(hava_durumu_bilgisi)

        await websocket.send(json.dumps(hava_durumu_bilgisi_list))

        time.sleep(60)


def start_websocket_server():
    start_server = websockets.serve(hava_durumu, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    start_websocket_server()
