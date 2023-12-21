import wx
import threading
from controllers.user_controller import UserController
from views.user_view import Register
from websocket_server import start_websocket_server


def run_gui():
    """
    GUI uygulamasını başlatır.

    Uygulamayı başlatır, kullanıcı kontrolcüsünü oluşturur ve kayıt sayfasını gösterir.
    """
    app = wx.App(False)
    controller = UserController()
    view = Register(controller)
    view.Show()
    app.MainLoop()


if __name__ == "__main__":
    # WebSocket sunucusunu ayrı bir thread'de başlat
    websocket_thread = threading.Thread(target=start_websocket_server)
    websocket_thread.start()

    # GUI uygulamasını ana thread'de çalıştır
    run_gui()

    # WebSocket thread'inin tamamlanmasını bekle
    websocket_thread.join()
