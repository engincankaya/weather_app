import wx
import os
import wx.lib.scrolledpanel as scrolled
import platform
from views.weather_view_details import WeatherDetailsFrame
from utils.utils import (
    capitalize_first_letter,
    create_temp_value_text,
    create_wind_value_text,
)


class WeatherApp(wx.Frame):
    def __init__(self, controller, user_fullname=None, *args, **kwds):
        # Hava Durumu Uygulaması görünümünün başlatılması
        super().__init__(
            parent=None,
            id=wx.ID_ANY,
            title="Hava Durumu Uygulaması",
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX),
        )
        self.controller = controller
        self.user_fullname = user_fullname
        self.weather_data_list = []
        self.selected_temp_unit = "Santigrat"

        os_name = platform.system()

        if os_name == "Windows":
            self.SetSize((500, 447))
        else:
            self.SetSize((350, 447))

        self.SetBackgroundColour(wx.Colour(34, 40, 49))
        self.scrolled_panel = scrolled.ScrolledPanel(self, wx.ID_ANY)
        self.scrolled_panel.SetupScrolling()

        self.create_ui()

    def create_ui(self):
        # Kullanıcı arayüzünü oluştur
        parent_sizer = wx.BoxSizer(wx.VERTICAL)
        self.create_navbar(parent_sizer)
        self.vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        parent_sizer.Add(self.vertical_sizer, 1, wx.EXPAND, 8)

        self.scrolled_panel.SetSizer(parent_sizer)
        if len(self.weather_data_list) == 0:
            loading_text = wx.StaticText(
                self.scrolled_panel,
                wx.ID_ANY,
                "Veriler Yükleniyor...",
                style=wx.ALIGN_LEFT,
            )
            loading_text.SetForegroundColour(wx.Colour(238, 238, 238))
            loading_text.SetFont(
                wx.Font(
                    15,
                    wx.FONTFAMILY_DECORATIVE,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD,
                    0,
                    "",
                )
            )
            self.vertical_sizer.Add(
                loading_text, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 8
            )
        self.Layout()

    def create_navbar(self, parent_sizer):
        # Navigasyon çubuğunu oluştur
        nav_bar = wx.BoxSizer(wx.HORIZONTAL)
        texts_sizer = wx.BoxSizer(wx.HORIZONTAL)
        parent_sizer.Add(nav_bar, 0, wx.ALL | wx.EXPAND, 5)
        parent_sizer.Add(texts_sizer, 0, wx.EXPAND)

        title_label = wx.StaticText(
            self.scrolled_panel, wx.ID_ANY, "24 Saatlik Veriler", style=wx.ALIGN_LEFT
        )
        title_label.SetForegroundColour(wx.Colour(238, 238, 238))
        title_label.SetFont(
            wx.Font(
                15,
                wx.FONTFAMILY_DECORATIVE,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD,
                0,
                "",
            )
        )
        nav_bar.Add(title_label, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 8)

        self.unit_combo_box = wx.ComboBox(
            self.scrolled_panel,
            wx.ID_ANY,
            choices=["Santigrat", "Fahrenhayt"],
            style=wx.CB_DROPDOWN,
        )
        self.unit_combo_box.SetMinSize((120, 20))
        self.unit_combo_box.Bind(wx.EVT_COMBOBOX, self.on_temperature_unit_change)
        nav_bar.Add(self.unit_combo_box, 0, 0, 0)

        info_text = wx.StaticText(
            self.scrolled_panel, wx.ID_ANY, "Veriler dakikada bir güncellenmektedir."
        )
        info_text.SetForegroundColour(wx.Colour(238, 238, 238))
        info_text.SetFont(
            wx.Font(
                10,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "",
            )
        )
        texts_sizer.Add(info_text, 0, wx.ALIGN_LEFT | wx.LEFT, 13)

        if self.user_fullname:
            user_fullname_text = wx.StaticText(
                self.scrolled_panel, wx.ID_ANY, self.user_fullname
            )
            user_fullname_text.SetForegroundColour(wx.Colour(238, 238, 238))
            user_fullname_text.SetFont(
                wx.Font(
                    10,
                    wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL,
                    0,
                    "",
                )
            )
            texts_sizer.Add(user_fullname_text, 0, wx.LEFT, 83)

    def on_temperature_unit_change(self, event):
        # Sıcaklık birim değişimine tepki ver
        self.selected_temp_unit = self.unit_combo_box.GetValue()
        wx.CallAfter(self.update_weather_view, self.weather_data_list)

    def update_weather_view(self, weather_data_list):
        # Hava durumu görünümünü güncelle
        self.weather_data_list = weather_data_list
        wx.CallAfter(self.generate_city_items)

    def generate_city_items(self):
        # Şehir öğelerini oluştur
        self.vertical_sizer.Clear(True)
        for data in self.weather_data_list:
            city_item_sizer = self.create_city_item(data, self.scrolled_panel)
            self.vertical_sizer.Add(city_item_sizer, 0, wx.EXPAND | wx.ALL, 20)

        self.scrolled_panel.Layout()
        self.scrolled_panel.SetupScrolling(scroll_x=False)
        self.scrolled_panel.SetVirtualSize(self.scrolled_panel.GetBestVirtualSize())

    def create_city_item(self, data, panel):
        # Şehir öğesini oluştur
        city_name = data["city_name"]
        temp = create_temp_value_text(self.selected_temp_unit, data["temp"])
        description = capitalize_first_letter(data["description"])
        wind = create_wind_value_text(data["wind"])
        icon = data["icon"].replace("n", "d")
        coord = f"E:{'{:.2f}'.format(data['coord']['lat'])}, B:{'{:.2f}'.format(data['coord']['lon'])}"

        city_item_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bitmap_11 = self.create_bitmap(panel, icon)
        city_item_sizer.Add(bitmap_11, 0, wx.ALIGN_CENTER_VERTICAL)

        grid_sizer = wx.GridSizer(3, 2, 7, 7)
        city_item_sizer.Add(grid_sizer, 2, wx.LEFT | wx.TOP, 20)

        labels = self.create_labels_for_grid_sizer(
            panel, temp, city_name, description, wind, coord
        )
        self.add_label_to_grid_sizer(grid_sizer, labels)

        if panel == self.scrolled_panel:
            button = wx.Button(panel, label="Detay")
            grid_sizer.Add(button, 0, wx.EXPAND)
            button.Bind(
                wx.EVT_BUTTON,
                lambda event, city_name=city_name: self.on_city_click(event, city_name),
            )

        return city_item_sizer

    def create_bitmap(self, panel, icon):
        # İcon resmini oluştur
        current_directory = os.getcwd()

        # İcon klasörünün yolu
        image_path = os.path.join(current_directory, "views", "icons", f"{icon}.png")
        image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
        image.Rescale(40, 40)
        bitmap = wx.Bitmap(image)
        bitmap_11 = wx.StaticBitmap(
            panel,
            wx.ID_ANY,
            bitmap,
        )
        return bitmap_11

    def add_label_to_grid_sizer(self, grid_sizer, labels):
        for label in labels:
            grid_sizer.Add(label, 0, 0, 0, 0)

    def create_labels_for_grid_sizer(
        self, panel, temp, city_name, description, wind, coord
    ):
        # Grid sizer için etiketleri oluştur
        temp_label = self.create_label(panel, temp, wx.Colour(0, 173, 181), 13, True)
        city_name_label = self.create_label(
            panel, city_name, wx.Colour(238, 238, 238), 13, True
        )
        description_label = self.create_label(
            panel, description, wx.Colour(238, 238, 238), 13, False
        )
        wind_label = self.create_label(panel, wind, wx.Colour(209, 209, 209), 12, False)
        coord_label = self.create_label(
            panel, coord, wx.Colour(209, 209, 209), 12, False
        )
        return [temp_label, city_name_label, description_label, wind_label, coord_label]

    def create_label(self, panel, text, color, font_size, bold):
        # Tek bir etiket oluştur
        label = wx.StaticText(panel, wx.ID_ANY, text)
        label.SetForegroundColour(color)
        font = wx.Font(
            font_size,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD if bold else wx.FONTWEIGHT_NORMAL,
            0,
            "",
        )
        label.SetFont(font)
        return label

    def on_city_click(self, event, city_name):
        # Şehir detaylarını göster
        details_frame = WeatherDetailsFrame(
            self, city_name, self.controller, self.selected_temp_unit
        )
        details_frame.Show()
