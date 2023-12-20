import wx
from controllers.weather_controller import WeatherController


if __name__ == "__main__":
    app = wx.App(False)
    controller = WeatherController()
    controller.run()
    app.MainLoop()
