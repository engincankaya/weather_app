import wx
from utils.utils import (
    capitalize_first_letter,
    timestamp_to_date,
    create_temp_value_text,
    create_wind_value_text,
    convert_temp_value,
)


class WeatherDetailsFrame(wx.Frame):
    def __init__(self, parent, city_name, controller, selected_temp_unit):
        # Hava Durumu Detayları penceresinin başlatılması
        super().__init__(
            parent,
            wx.ID_ANY,
            "Weather Details",
            size=(800, 320),
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX),
        )
        self.SetTitle(f"{city_name} Detaylı Bilgiler")
        self.controller = controller
        self.parent_view = parent
        self.selected_temp_unit = selected_temp_unit
        self.city_data = self.get_city_weather_infos(city_name)

        # Ana panelin oluşturulması
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.setup_layout()

    def setup_layout(self):
        # Ana sizer'ı oluştur
        parent_sizer = wx.BoxSizer(wx.VERTICAL)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Bugünkü bilgileri WeatherApp sınıfından oluştur
        today_infos = self.parent_view.create_city_item(self.city_data, self.panel_1)
        top_sizer.Add(today_infos, 1, wx.EXPAND, 0)

        # Geçen yılın bilgilerini ekle
        last_year_infos = self.create_last_year_layout()
        top_sizer.Add(last_year_infos, 1, wx.EXPAND, 0)

        parent_sizer.Add(top_sizer, 1, wx.EXPAND | wx.LEFT, 7)

        # Takip eden günlerin bilgilerini ekle
        following_days_sizer = wx.BoxSizer(wx.HORIZONTAL)
        parent_sizer.Add(following_days_sizer, 2, wx.EXPAND, 0)
        self.create_following_days(following_days_sizer)

        # Panel için ana sizer'ı ayarla
        self.panel_1.SetSizer(parent_sizer)
        self.Layout()

    def create_last_year_layout(self):
        date = timestamp_to_date(self.city_data["last_year_data"]["date"])
        temp_last_year = convert_temp_value(
            self.selected_temp_unit, self.city_data["last_year_data"]["temp"]
        )
        temp_today = convert_temp_value(self.selected_temp_unit, self.city_data["temp"])
        temp_difference = (temp_last_year) - temp_today
        temp_text = self.extract_temp_difference_text(temp_last_year, temp_difference)

        description = self.city_data["last_year_data"]["description"]
        description = capitalize_first_letter(description)
        wind = create_wind_value_text(self.city_data["last_year_data"]["wind"])
        # Geçen yılın bilgileri ile karşılaştırma için düzeni oluştur
        last_year_infos = wx.StaticBoxSizer(
            wx.StaticBox(self.panel_1, wx.ID_ANY, ""), wx.VERTICAL
        )

        title = wx.StaticText(
            self.panel_1, wx.ID_ANY, "Geçen Yıl Değerleri ile Kıyaslama"
        )
        self.set_label_properties(title, 14, wx.Colour(0, 173, 181), wx.FONTWEIGHT_BOLD)
        last_year_infos.Add(title, 0, wx.BOTTOM | wx.EXPAND, 10)

        # Geçen yılın verileri için grid sizer ekliyoruz.
        grid_sizer = wx.GridSizer(2, 2, 0, 0)
        last_year_infos.Add(grid_sizer, 1, wx.EXPAND, 0)

        # Geçen yılın verilerinin etiketlerini ekliyoruz.
        date_label = wx.StaticText(self.panel_1, wx.ID_ANY, f"Tarih: {date}")
        temp_label = wx.StaticText(self.panel_1, wx.ID_ANY, f"Sıcaklık:{temp_text}")
        description_label = wx.StaticText(
            self.panel_1, wx.ID_ANY, f"Durum: {description}"
        )
        wind_label = wx.StaticText(self.panel_1, wx.ID_ANY, f"Rüzgar: {wind}")

        # Etiketleri grid sizer'a ekliyoruz.
        grid_sizer.Add(date_label, 0, 0, 0)
        grid_sizer.Add(temp_label, 0, 0, 0)
        grid_sizer.Add(description_label, 0, 0, 0)
        grid_sizer.Add(wind_label, 0, 0, 0)

        return last_year_infos

    def extract_temp_difference_text(self, temp_last_year, temp_difference):
        # Sıcaklık farkı metnini çıkart
        if self.selected_temp_unit == "Santigrat":
            if temp_difference > 0:
                text = f"{temp_last_year}°C (+{temp_difference}°C daha sıcak)"
            else:
                text = f"{temp_last_year}°C (-{temp_difference}°C daha soğuk)"
        else:
            if temp_difference > 0:
                text = f"{temp_last_year}°F (+{temp_difference}°F daha sıcak)"
            else:
                text = f"{temp_last_year}°F (-{temp_difference}°F daha soğuk)"
        return text

    def create_following_days(self, following_days_sizer):
        # Takip eden günlerin bilgilerini oluşturma
        for data in self.city_data["following_days"]:
            following_day_infos = self.create_following_day_layout(data)
            following_days_sizer.Add(following_day_infos, 1, wx.EXPAND, 0)

    def create_following_day_layout(self, data):
        date = timestamp_to_date(data["date"])
        temp = create_temp_value_text(self.selected_temp_unit, data["temp"])
        description = capitalize_first_letter(data["description"])
        icon = data["icon"].replace("n", "d")
        wind_text = create_wind_value_text(self.city_data["wind"])

        # Her takip eden gün bilgisi için düzeni oluşturma
        following_day_infos = wx.StaticBoxSizer(
            wx.StaticBox(self.panel_1, wx.ID_ANY, ""), wx.VERTICAL
        )

        # Hava durumu ikonunu ekle(Fonksiyonu WeatherApp classından çekiyoruz.)
        icon_bitmap = self.parent_view.create_bitmap(self.panel_1, icon)
        following_day_infos.Add(icon_bitmap, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        # Tarih ve hava detaylarını ekleme
        infos_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        following_day_infos.Add(infos_vertical_sizer, 1, wx.EXPAND | wx.TOP, 13)

        date = wx.StaticText(self.panel_1, wx.ID_ANY, date)
        temp = wx.StaticText(self.panel_1, wx.ID_ANY, temp)
        description = wx.StaticText(self.panel_1, wx.ID_ANY, description)
        wind_label = wx.StaticText(self.panel_1, wx.ID_ANY, "Rüzgar:")
        wind = wx.StaticText(
            self.panel_1, wx.ID_ANY, wind_text, style=wx.ALIGN_CENTER_HORIZONTAL
        )
        # Etiketler için özellikleri ayarlama
        self.set_label_properties(
            date, 13, wx.Colour(238, 238, 238), wx.FONTWEIGHT_BOLD
        )
        self.set_label_properties(temp, 13, wx.Colour(0, 173, 181), wx.FONTWEIGHT_BOLD)
        self.set_label_properties(
            description, 12, wx.Colour(209, 209, 209), wx.FONTWEIGHT_NORMAL
        )

        # Etiketleri sizer'a ekleme
        infos_vertical_sizer.Add(date, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)

        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        infos_vertical_sizer.Add(sizer_1, 1, wx.SHAPED, 0)
        sizer_1.Add(temp, 1, 0, wx.EXPAND, 0)
        sizer_1.Add(description, 1, wx.BOTTOM, 2)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        infos_vertical_sizer.Add(sizer_2, 1, wx.EXPAND, 0)

        # Etiketler için özellikleri ayarla
        self.set_label_properties(
            wind_label, 13, wx.Colour(238, 238, 238), wx.FONTWEIGHT_NORMAL
        )
        self.set_label_properties(
            wind, 12, wx.Colour(209, 209, 209), wx.FONTWEIGHT_NORMAL
        )

        # Etiketleri sizer'a ekleme
        sizer_2.Add(wind_label, 1, 0, 0)
        sizer_2.Add(wind, 2, wx.LEFT, 3)

        return following_day_infos

    def set_label_properties(self, label, font_size, text_color, font_weight):
        # Etiketler için ortak özellikleri ayarla
        label.SetForegroundColour(text_color)
        label.SetFont(
            wx.Font(
                font_size,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                font_weight,
                0,
                "",
            )
        )

    def get_city_weather_infos(self, city_name):
        return self.controller.search_detailed_infos_by_name(city_name)
