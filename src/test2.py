import wx
import threading
import time

# 250, 447


class WeatherApp(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.panel = wx.Panel(self)
        self_vertical_layout = wx.BoxSizer(wx.VERTICAL)
        button1 = wx.Button(self_vertical_layout, Fla)

    def on_close(self, event):
        self.Destroy()

    def update_weather_view(self, weather_data_list):
        wx.CallAfter(self._update_weather_view, weather_data_list)

    def _update_weather_view(self, weather_data_list):
        # Clear the existing content before updating with new data
        self.text_ctrl.Clear()
