import wx
import wx.lib.scrolledpanel as scrolled
from views.weather_view_details import WeatherDetailsFrame


class WeatherApp(wx.Frame):
    def __init__(self, controller, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        kwds["style"] &= ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        super().__init__(parent=None, id=wx.ID_ANY, title="Hava Durumu Uygulaması")
        self.controller = controller

        self.SetSize((280, 447))
        self.SetTitle("Weather App")
        self.SetBackgroundColour(wx.Colour(34, 40, 49))

        self.scrolled_panel = scrolled.ScrolledPanel(self, wx.ID_ANY)
        self.scrolled_panel.SetupScrolling()

        parent_sizer = wx.BoxSizer(wx.VERTICAL)

        self.create_navbar(parent_sizer)

        self.vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        parent_sizer.Add(self.vertical_sizer, 1, wx.EXPAND, 8)

        self.scrolled_panel.SetSizer(parent_sizer)
        self.Layout()

    def create_navbar(self, parent_sizer):
        nav_bar = wx.BoxSizer(wx.HORIZONTAL)
        parent_sizer.Add(nav_bar, 0, wx.ALL | wx.EXPAND, 5)

        label_4 = wx.StaticText(
            self.scrolled_panel, wx.ID_ANY, "24 Saatlik ", style=wx.ALIGN_LEFT
        )
        label_4.SetForegroundColour(wx.Colour(238, 238, 238))
        label_4.SetFont(
            wx.Font(
                15,
                wx.FONTFAMILY_DECORATIVE,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD,
                0,
                "",
            )
        )
        nav_bar.Add(label_4, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 8)

        self.combo_box_2 = wx.ComboBox(
            self.scrolled_panel,
            wx.ID_ANY,
            choices=["Santigrat", "Fahrenhayt"],
            style=wx.CB_DROPDOWN,
        )
        self.combo_box_2.SetMinSize((120, 20))
        nav_bar.Add(self.combo_box_2, 0, 0, 0)

        sayac = wx.StaticText(self.scrolled_panel, wx.ID_ANY, "Yenilenme: 15s")
        sayac.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                ".AppleSystemUIFont",
            )
        )
        parent_sizer.Add(sayac, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 6)

    def update_weather_view(self, weather_data_list):
        wx.CallAfter(self.generate_city_items, weather_data_list)

    def generate_city_items(self, weather_data_list):
        self.vertical_sizer.Clear(True)
        for data in weather_data_list:
            vertical_sizer_item = self.create_city_item(data)
            self.vertical_sizer.Add(vertical_sizer_item, 0, wx.EXPAND | wx.ALL, 10)
        self.scrolled_panel.Layout()
        self.scrolled_panel.SetupScrolling(scroll_x=False)
        self.scrolled_panel.SetVirtualSize(self.scrolled_panel.GetBestVirtualSize())

    def create_city_item(self, data):
        city_name = data["city_name"]
        temp = f"{data['temp']}°C"
        desp = data["description"]
        wind = f"{data['wind']['speed']} m/s, {data['wind']['deg']}°"

        vertical_sizer_item = wx.BoxSizer(wx.HORIZONTAL)

        bitmap_11 = self.create_bitmap()
        vertical_sizer_item.Add(bitmap_11, 0, wx.ALIGN_CENTER_VERTICAL)

        item_right_side = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer_item.Add(item_right_side, 2, wx.EXPAND | wx.LEFT, 20)

        top_infos_sizer = self.create_top_infos_sizer(temp, city_name)
        item_right_side.Add(top_infos_sizer, 1, wx.BOTTOM | wx.EXPAND | wx.RIGHT, 7)

        label_35 = self.create_description_label(desp)
        item_right_side.Add(label_35, 1, wx.BOTTOM, 2)

        bottom_infos_sizer = self.create_bottom_infos_sizer(wind)
        item_right_side.Add(bottom_infos_sizer, 1, wx.EXPAND | wx.RIGHT, 7)

        return vertical_sizer_item

    def create_bitmap(self):
        bitmap_11 = wx.StaticBitmap(
            self.scrolled_panel,
            wx.ID_ANY,
            wx.Bitmap(
                "/Users/engincankaya/Desktop/resimler/sunny.png", wx.BITMAP_TYPE_ANY
            ),
        )
        bitmap_11.SetMinSize((40, 40))
        return bitmap_11

    def create_top_infos_sizer(self, temp, city_name):
        top_infos_sizer = wx.BoxSizer(wx.HORIZONTAL)

        label_33 = self.create_label(temp, wx.Colour(0, 173, 181), 13, True)
        top_infos_sizer.Add(label_33, 1, 0, 0)

        label_34 = self.create_label(city_name, wx.Colour(238, 238, 238), 13, True)
        label_34.Bind(
            wx.EVT_LEFT_DOWN,
            lambda event, city_name=city_name: self.on_city_click(event, city_name),
        )
        top_infos_sizer.Add(label_34, 2, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 3)

        return top_infos_sizer

    def create_description_label(self, desp):
        label_35 = self.create_label(desp, wx.Colour(209, 209, 209), 12, False)
        return label_35

    def create_bottom_infos_sizer(self, wind):
        bottom_infos_sizer = wx.BoxSizer(wx.HORIZONTAL)

        Ruzgar_copy_7 = self.create_label(
            "Rüzgar:", wx.Colour(238, 238, 238), 13, False
        )
        bottom_infos_sizer.Add(Ruzgar_copy_7, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        label_41 = self.create_label(wind, wx.Colour(209, 209, 209), 12, False)
        bottom_infos_sizer.Add(label_41, 2, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 3)

        return bottom_infos_sizer

    def create_label(self, text, color, font_size, bold):
        label = wx.StaticText(self.scrolled_panel, wx.ID_ANY, text)
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
        details_frame = WeatherDetailsFrame(self, city_name, self.controller)
        details_frame.Show()
