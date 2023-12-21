from threading import Thread
import websocket
import json
import wx
from models.weather_model import WeatherModel
from views.weather_view import WeatherApp
from dotenv import load_dotenv
import os

load_dotenv()


class WeatherController:
    def __init__(self, user_fullname=False):
        # WeatherController'ın başlatılması
        self.model = WeatherModel()
        self.view = WeatherApp(self, user_fullname)
        self.ws = WeatherWsController(self)
        self.ws_thread = Thread(target=self.ws.run_forever)
        self.ws_thread.start()

    def update_weather(self, data_list):
        # Hava durumu verilerini ve görünümü güncelle
        for data in data_list:
            self.model.create_or_update(data)
        weather_data_list = self.model.get_all_cities_main_weather_datas()
        wx.CallAfter(self.view.update_weather_view(weather_data_list))

    def search_detailed_infos_by_name(self, city_name):
        # Şehir adına göre detaylı bilgileri ara
        return self.model.get_detailed_infos_by_name(city_name)

    def run(self):
        # Uygulamayı başlat
        self.view.Show()


class WeatherWsController:
    def __init__(self, controller):
        # Weather WebSocket Controller'ın başlatılması
        self.controller = controller
        self.port = os.getenv("PORT")
        self.ws = websocket.WebSocketApp(
            f"ws://localhost:{self.port}",
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close,
        )

    def on_message(self, ws, message):
        # WebSocket üzerinden gelen mesajı işle
        try:
            weather_data_list = json.loads(message)
            self.controller.update_weather(weather_data_list)

        except json.JSONDecodeError as e:
            print(f"JSON Çözme Hatası: {e}")

    def on_open(self, ws):
        # Bağlantı açıldığında yapılacak işlemler
        print("Bağlantı açıldı")

    def on_error(self, ws, error):
        # WebSocket hatası
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        # Bağlantı kapandığında yapılacak işlemler
        print(f"{close_status_code} - {close_msg}")

    def run_forever(self, reconnect=5):
        # WebSocket bağlantısını sürekli olarak dinleniyor
        self.ws.run_forever(reconnect=reconnect)
