import wx
import threading
from controllers.weather_controller import WeatherController
from controllers.user_controller import UserController
from views.user_view import Register
from websocket_server import start_websocket_server


def run_gui():
    app = wx.App(False)
    controller = UserController()
    view = Register(controller)
    view.Show()
    app.MainLoop()


if __name__ == "__main__":
    # Start the WebSocket server in a separate thread
    websocket_thread = threading.Thread(target=start_websocket_server)
    websocket_thread.start()

    # Run the GUI application in the main thread
    run_gui()

    # Wait for the WebSocket thread to finish
    websocket_thread.join()
