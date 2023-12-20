from threading import Thread
import websocket
import json
import wx
from models.weather_model import WeatherModel
from views.weather_view import WeatherApp


class WeatherController:
    def __init__(self):
        self.model = WeatherModel()
        self.view = WeatherApp(self)
        self.ws = WeatherWsController(self)
        self.ws_thread = Thread(target=self.ws.run_forever)
        self.ws_thread.start()

    def update_weather(self, data_list):
        for data in data_list:
            self.model.create_or_update(data)
        weather_data_list = self.model.get_all_cities_main_weather_datas()
        wx.CallAfter(self.view.update_weather_view(weather_data_list))

    def search_detailed_infos_by_name(self, city_name):
        return self.model.get_detailed_infos_by_name(city_name)

    def run(self):
        self.view.Show()

    # def on_close(self):
    #     self.model.ws.close()
    #     self.model_thread.join()

    # def get_latest_weather_data(self):
    #     return self.model.to_dict


class WeatherWsController:
    def __init__(self, controller):
        self.controller = controller
        self.ws = websocket.WebSocketApp(
            "ws://localhost:8765",
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close,
        )

    def on_message(self, ws, message):
        try:
            weather_data_list = json.loads(message)
            self.controller.update_weather(weather_data_list)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def on_open(self, ws):
        print("Opened connection")

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"{close_status_code} - {close_msg}")

    def run_forever(self, reconnect=5):
        self.ws.run_forever(reconnect=reconnect)

    # def set_latest_weather_data(self, data):
    #     self.weather_data = self.model(data)
