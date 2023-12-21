import wx
import os
from utils.utils import switch_page


class UserView(wx.Frame):
    def __init__(self, controller, *args, **kwds):
        super().__init__(
            parent=None,
            id=wx.ID_ANY,
            title="Üyelik İşlemleri",
            size=(477, 442),
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX),
        )
        self.controller = controller
        self.SetBackgroundColour(wx.Colour(34, 40, 49))
        self.main_panel = wx.Panel(self, wx.ID_ANY)
        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.content_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.footer_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.create_ui()

    def create_ui(self):
        current_directory = os.getcwd()
        app_logo_path = os.path.join(
            current_directory, "views", "icons", "app_logo.png"
        )
        image = wx.Image(app_logo_path, wx.BITMAP_TYPE_ANY)
        image.Rescale(120, 106)
        bitmap = wx.Bitmap(image)
        header_bitmap = wx.StaticBitmap(
            self.main_panel,
            wx.ID_ANY,
            bitmap,
        )
        self.header_vertical_sizer.Add(
            header_bitmap,
            0,
            wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.TOP,
            23,
        )

        header_label = wx.StaticText(self.main_panel, wx.ID_ANY, "Weather App")
        header_label.SetForegroundColour(wx.Colour(238, 238, 238))
        header_label.SetFont(
            wx.Font(
                13,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD,
                0,
                "",
            )
        )
        self.header_vertical_sizer.Add(
            header_label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 9
        )

        self.main_vertical_sizer.Add(self.header_vertical_sizer, 1, wx.EXPAND, 0)

        self.main_vertical_sizer.Add(
            self.content_vertical_sizer, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20
        )

        self.main_vertical_sizer.Add(self.footer_vertical_sizer, 1, wx.EXPAND, 0)

        self.main_panel.SetSizer(self.main_vertical_sizer)
        self.main_panel.Layout()

    def display_error(self, error_message):
        wx.MessageBox(error_message, "Error", wx.OK | wx.ICON_ERROR)


class Login(UserView):
    def __init__(self, controller):
        super(Login, self).__init__(controller)
        self.controller.view = self
        self.email_text_ctrl = wx.TextCtrl(
            self.main_panel, wx.ID_ANY, style=wx.TE_CENTRE
        )
        self.password_text_ctrl = wx.TextCtrl(
            self.main_panel, wx.ID_ANY, style=wx.TE_CENTRE | wx.TE_PASSWORD
        )
        self.login_button = wx.Button(self.main_panel, wx.ID_ANY, "Giriş Yap")
        self.setup_login_ui()

    def setup_login_ui(self):
        self.email_text_ctrl.SetMinSize((300, 30))
        self.password_text_ctrl.SetMinSize((300, 30))
        self.login_button.SetMinSize((300, 30))
        self.login_button.SetBackgroundColour(wx.Colour(0, 91, 95))
        self.email_text_ctrl.SetHint("Email Adresiniz")
        self.password_text_ctrl.SetHint("Şifreniz")

        self.content_vertical_sizer.Add(self.email_text_ctrl, 1, wx.EXPAND, 0)
        self.content_vertical_sizer.Add(
            self.password_text_ctrl, 1, wx.EXPAND | wx.TOP, 4
        )

        self.footer_vertical_sizer.Add(
            self.login_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0
        )

        register_label = wx.StaticText(
            self.main_panel, wx.ID_ANY, "Üyeliğiniz Yok Mu? Üye Ol"
        )
        register_label.SetForegroundColour(wx.Colour(50, 50, 204))
        register_label.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD,
                1,
                "",
            )
        )
        register_label.Bind(
            wx.EVT_LEFT_DOWN,
            lambda event: switch_page(
                self.Hide, Register(self.controller).Show, event.Skip
            ),
        )
        self.footer_vertical_sizer.Add(
            register_label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 7
        )
        self.login_button.Bind(wx.EVT_BUTTON, self.on_login_button_click)

    def on_login_button_click(self, event):
        email = self.email_text_ctrl.GetValue()
        password = self.password_text_ctrl.GetValue()
        self.controller.login(email, password)


class Register(UserView):
    def __init__(self, controller):
        super(Register, self).__init__(controller)
        self.controller = controller
        self.controller.view = self
        self.fullname_text_ctrl = wx.TextCtrl(
            self.main_panel, wx.ID_ANY, style=wx.TE_CENTRE
        )
        self.email_text_ctrl = wx.TextCtrl(
            self.main_panel, wx.ID_ANY, style=wx.TE_CENTRE
        )
        self.password_text_ctrl = wx.TextCtrl(
            self.main_panel, wx.ID_ANY, style=wx.TE_CENTRE | wx.TE_PASSWORD
        )

        self.register_button = wx.Button(self.main_panel, wx.ID_ANY, "Kayıt Ol")
        self.setup_register_ui()

    def setup_register_ui(self):
        self.fullname_text_ctrl.SetMinSize((300, 30))
        self.email_text_ctrl.SetMinSize((300, 30))
        self.password_text_ctrl.SetMinSize((300, 30))
        self.register_button.SetMinSize((300, 30))
        self.register_button.SetBackgroundColour(wx.Colour(0, 91, 95))
        self.fullname_text_ctrl.SetHint("İsim ve Soyisim")
        self.email_text_ctrl.SetHint("Email Adresiniz")
        self.password_text_ctrl.SetHint("Şifreniz")

        self.content_vertical_sizer.Add(self.fullname_text_ctrl, 1, wx.EXPAND, 0)
        self.content_vertical_sizer.Add(self.email_text_ctrl, 1, wx.EXPAND | wx.TOP, 4)
        self.content_vertical_sizer.Add(
            self.password_text_ctrl, 1, wx.EXPAND | wx.TOP, 4
        )

        self.footer_vertical_sizer.Add(
            self.register_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0
        )

        login_label = wx.StaticText(
            self.main_panel, wx.ID_ANY, "Üyeliğiniz Var Mı? Giriş Yap"
        )
        login_label.SetForegroundColour(wx.Colour(50, 50, 204))
        login_label.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD,
                1,
                "",
            )
        )
        login_label.Bind(
            wx.EVT_LEFT_DOWN,
            lambda event: switch_page(
                self.Hide, Login(self.controller).Show, event.Skip
            ),
        )
        self.footer_vertical_sizer.Add(
            login_label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 7
        )
        self.register_button.Bind(wx.EVT_BUTTON, self.on_register_button_click)

    def on_register_button_click(self, event):
        fullname = self.fullname_text_ctrl.GetValue()
        email = self.email_text_ctrl.GetValue()
        password = self.password_text_ctrl.GetValue()
        self.controller.create_account(fullname, email, password)
