from models.weather_model import WeatherModel
from views.weather_view import WeatherApp
from controllers.weather_controller import WeatherController
import wx
import traceback


if __name__ == "__main__":
    app = wx.App(False)
    view = WeatherApp(None, wx.ID_ANY, "Hava Durumu Uygulaması")
    view.Show()
    controller = WeatherController(view)

    app.MainLoop()
    traceback.print_exc()
