from models.user_model import UserModel
from controllers.weather_controller import WeatherController


class UserController:
    def __init__(self):
        self.model = UserModel
        self.view = None

    def create_account(self, fullname, email, password):
        # Hesap oluşturma isteğini model'e yolla
        error_message = self.model.create_account(fullname, email, password)
        if error_message:
            # Hata mesajını görüntüle
            self.view.display_error(error_message)
        else:
            # Üyelik işlemi başarılıysa anasayfaya yolla
            self.send_main_page(fullname)

    def login(self, email, password):
        # Kullanıcı girişi yapma isteğini model'e yolla
        error_message = self.model.user_login(email, password)
        if error_message:
            # Hata mesajını görüntüle
            self.view.display_error(error_message)
        else:
            # Giriş işlemi başarılıysa anasayfaya yolla
            user_fullname = self.model.get_user_name(email)
            self.send_main_page(user_fullname)

    def send_main_page(self, user_fullname):
        # Ana sayfaya yönlendir
        self.view.Hide()
        controller = WeatherController(user_fullname)
        controller.run()
