import wx
import wx.lib.scrolledpanel as scrolled


class WeatherDetailsFrame(wx.Frame):
    def __init__(self, parent, city_data):
        super().__init__(parent, wx.ID_ANY, "Weather Details", size=(300, 200))
        panel = wx.Panel(self)

        # Display the weather details for the clicked city
        wx.StaticText(panel, wx.ID_ANY, f"City: {city_data['city_name']}", pos=(10, 10))
        wx.StaticText(
            panel, wx.ID_ANY, f"Temperature: {city_data['temp']}°C", pos=(10, 30)
        )
        wx.StaticText(
            panel, wx.ID_ANY, f"Description: {city_data['description']}", pos=(10, 50)
        )
        wx.StaticText(
            panel,
            wx.ID_ANY,
            f"Wind: {city_data['wind']['speed']} m/s, {city_data['wind']['deg']}°",
            pos=(10, 70),
        )


class WeatherApp(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        kwds["style"] &= ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        super().__init__(*args, **kwds)

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
        wx.CallAfter(self.create_vertical_sizer_item, weather_data_list)

    def create_vertical_sizer_item(self, weather_data_list):
        self.vertical_sizer.Clear(True)
        for data in weather_data_list:
            city_name = data["city_name"]
            temp = f"{data['temp']}°C"
            desp = data["description"]
            wind = f"{data['wind']['speed']} m/s, {data['wind']['deg']}°"

            vertical_sizer_item = wx.BoxSizer(wx.HORIZONTAL)
            self.vertical_sizer.Add(vertical_sizer_item, 0, wx.EXPAND | wx.ALL, 10)

            bitmap_11 = wx.StaticBitmap(
                self.scrolled_panel,
                wx.ID_ANY,
                wx.Bitmap(
                    "/Users/engincankaya/Desktop/resimler/sunny.png",
                    wx.BITMAP_TYPE_ANY,
                ),
            )
            bitmap_11.SetMinSize((40, 40))
            vertical_sizer_item.Add(bitmap_11, 0, wx.ALIGN_CENTER_VERTICAL)

            item_right_side = wx.BoxSizer(wx.VERTICAL)
            vertical_sizer_item.Add(item_right_side, 2, wx.EXPAND | wx.LEFT, 20)

            top_infos_sizer = wx.BoxSizer(wx.HORIZONTAL)
            item_right_side.Add(top_infos_sizer, 1, wx.BOTTOM | wx.EXPAND | wx.RIGHT, 7)

            label_33 = wx.StaticText(self.scrolled_panel, wx.ID_ANY, temp)
            label_33.SetForegroundColour(wx.Colour(0, 173, 181))
            label_33.SetFont(
                wx.Font(
                    13,
                    wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD,
                    0,
                    "",
                )
            )
            top_infos_sizer.Add(label_33, 1, 0, 0)

            label_34 = wx.StaticText(
                self.scrolled_panel,
                wx.ID_ANY,
                city_name,
                style=wx.ALIGN_CENTER_HORIZONTAL,
            )
            label_34.SetForegroundColour(wx.Colour(238, 238, 238))
            label_34.SetFont(
                wx.Font(
                    13,
                    wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD,
                    0,
                    "",
                )
            )
            label_34.Bind(
                wx.EVT_LEFT_DOWN,
                lambda event, city_data=data: self.on_city_click(event, city_data),
            )

            top_infos_sizer.Add(label_34, 2, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 3)

            label_35 = wx.StaticText(self.scrolled_panel, wx.ID_ANY, desp)
            label_35.SetForegroundColour(wx.Colour(209, 209, 209))
            label_35.SetFont(
                wx.Font(
                    12,
                    wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL,
                    0,
                    "",
                )
            )
            item_right_side.Add(label_35, 1, wx.BOTTOM, 2)

            bottom_infos_sizer = wx.BoxSizer(wx.HORIZONTAL)
            item_right_side.Add(bottom_infos_sizer, 1, wx.EXPAND | wx.RIGHT, 7)

            Ruzgar_copy_7 = wx.StaticText(self.scrolled_panel, wx.ID_ANY, "Rüzgar:")
            Ruzgar_copy_7.SetForegroundColour(wx.Colour(238, 238, 238))
            Ruzgar_copy_7.SetFont(
                wx.Font(
                    13,
                    wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL,
                    0,
                    "",
                )
            )
            bottom_infos_sizer.Add(Ruzgar_copy_7, 1, wx.ALIGN_CENTER_VERTICAL, 0)

            label_41 = wx.StaticText(
                self.scrolled_panel, wx.ID_ANY, wind, style=wx.ALIGN_CENTER_HORIZONTAL
            )
            label_41.SetForegroundColour(wx.Colour(209, 209, 209))
            label_41.SetFont(
                wx.Font(
                    12,
                    wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL,
                    0,
                    "",
                )
            )
            bottom_infos_sizer.Add(label_41, 2, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 3)
        self.scrolled_panel.Layout()
        self.scrolled_panel.SetupScrolling(scroll_x=False)
        self.scrolled_panel.SetVirtualSize(self.scrolled_panel.GetBestVirtualSize())

    def on_city_click(self, event, city_data):
        details_frame = WeatherDetailsFrame(self, city_data)
        details_frame.Show()
