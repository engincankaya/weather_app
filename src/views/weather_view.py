import wx
import threading
import time


class DetailDialog(wx.Dialog):
    def __init__(self, parent, title, weather_data):
        super(DetailDialog, self).__init__(parent, title=title, size=(400, 300))

        self.weather_data = weather_data

        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Detaylı bilgileri burada görüntüle, örneğin:
        detail_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        detail_text.AppendText(f"Şehir: {self.weather_data['city_name']}\n")
        detail_text.AppendText(f"Sıcaklık: {self.weather_data['temp']} °C\n")
        detail_text.AppendText(f"Durum: {self.weather_data['description']}\n")
        detail_text.AppendText(
            f"Rüzgar: {self.weather_data['wind']['speed']} m/s, {self.weather_data['wind']['deg']}°\n"
        )
        detail_text.AppendText(
            f"Gün doğumu: {wx.DateTime.FromTimeT(self.weather_data['sunrise']).Format('%H:%M:%S')}\n"
        )
        detail_text.AppendText(
            f"Gün batımı: {wx.DateTime.FromTimeT(self.weather_data['sunset']).Format('%H:%M:%S')}\n"
        )
        detail_text.AppendText(f"Şuan: {self.weather_data['creation_date']}")

        sizer.Add(detail_text, 1, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(sizer)

        self.Centre()
        self.ShowModal()
        self.Destroy()


class WeatherApp(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.panel = wx.Panel(self)
        self.text_ctrl = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Örneğin, bu alanda weather_data_list'i tanımlayın
        self.weather_data_list = []

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(sizer)
        self.SetSize((800, 600))
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Tıklama olayını ekleyin
        self.text_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.show_detail)

    def on_close(self, event):
        self.Destroy()

    def update_weather_view(self, weather_data_list):
        wx.CallAfter(self._update_weather_view, weather_data_list)

    def _update_weather_view(self, weather_data_list):
        # Clear the existing content before updating with new data
        self.text_ctrl.Clear()

        # Güncellenen verileri sakla
        self.weather_data_list = weather_data_list

        try:
            for weather_data in weather_data_list:
                data_line = (
                    f"Şehir: {weather_data['city_name']} | "
                    f"Sıcaklık: {weather_data['temp']} °C | "
                    f"Durum: {weather_data['description']} | "
                    f"Rüzgar: {weather_data['wind']['speed']} m/s, {weather_data['wind']['deg']}° | "
                    f"Gün doğumu: {wx.DateTime.FromTimeT(weather_data['sunrise']).Format('%H:%M:%S')} | "
                    f"Gün batımı: {wx.DateTime.FromTimeT(weather_data['sunset']).Format('%H:%M:%S')} | "
                    f"Şuan: {weather_data['creation_date']}\n\n"
                )
                self.text_ctrl.AppendText(data_line)
        except Exception as e:
            print(f"Hata: {e}")

    def show_detail(self, event):
        # GetInsertionPoint metodu ile tıklanan konumu alın
        position = self.text_ctrl.GetInsertionPoint()

        # Kontrol ekleyerek hata önleme
        if position < len(self.weather_data_list) * 2:
            # İlgili hava durumu verisini alın
            selected_weather_data = self.weather_data_list[position // 2]

            # Detay penceresini gösterin
            detail_dialog = DetailDialog(
                self, "Detaylı Bilgiler", selected_weather_data
            )
