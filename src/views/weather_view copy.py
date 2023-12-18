import wx
import threading
import time


class WeatherApp(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.panel = wx.Panel(self)
        self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(sizer)
        self.SetSize((800, 600))
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Destroy()

    def update_weather_view(self, weather_data_list):
        wx.CallAfter(self._update_weather_view, weather_data_list)

    def _update_weather_view(self, weather_data_list):
        # Clear the existing content before updating with new data
        self.text_ctrl.Clear()

        try:
            for weather_data in weather_data_list:
                self.text_ctrl.AppendText(f"Şehir: {weather_data['city_name']}\n")
                self.text_ctrl.AppendText(f"Sıcaklık: {weather_data['temp']} °C\n")
                self.text_ctrl.AppendText(f"Durum: {weather_data['description']}\n")
                wind_info = f"Rüzgar: {weather_data['wind']['speed']} m/s, {weather_data['wind']['deg']}°\n"
                self.text_ctrl.AppendText(wind_info)
                sunrise_time = wx.DateTime.FromTimeT(weather_data["sunrise"]).Format(
                    "%H:%M:%S"
                )
                sunset_time = wx.DateTime.FromTimeT(weather_data["sunset"]).Format(
                    "%H:%M:%S"
                )
                self.text_ctrl.AppendText(f"Gün doğumu: {sunrise_time}\n")
                self.text_ctrl.AppendText(f"Gün batımı: {sunset_time}\n")
                self.text_ctrl.AppendText(f"Şuan: {weather_data['creation_date']}\n")
                self.text_ctrl.AppendText("\n")
        except Exception as e:
            print(f"Hata: {e}")
