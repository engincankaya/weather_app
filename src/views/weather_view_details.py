import wx


class WeatherDetailsFrame(wx.Frame):
    def __init__(self, parent, city_name, controller):
        super().__init__(parent, wx.ID_ANY, "Weather Details", size=(300, 200))
        panel = wx.Panel(self)
        self.controller = controller
        self.city_data = self.get_city_weather_infos(city_name)
        if self.city_data:
            print(self.city_data)
            # Display the weather details for the clicked city
            wx.StaticText(
                panel, wx.ID_ANY, f"City: {self.city_data['city_name']}", pos=(10, 10)
            )
            wx.StaticText(
                panel,
                wx.ID_ANY,
                f"Temperature: {self.city_data['temp']}°C",
                pos=(10, 30),
            )
            wx.StaticText(
                panel,
                wx.ID_ANY,
                f"Description: {self.city_data['description']}",
                pos=(10, 50),
            )
            wx.StaticText(
                panel,
                wx.ID_ANY,
                f"Wind: {self.city_data['wind']['speed']} m/s, {self.city_data['wind']['deg']}°",
                pos=(10, 70),
            )

    def get_city_weather_infos(self, city_name):
        return self.controller.search_detailed_infos_by_name(city_name)
