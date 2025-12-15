# /home/xty/Documents/Projects/PetProject/BomberBot_GUI/BomberBot_GUI/app.py
import sys
import asyncio
from qasync import QEventLoop
from PySide6.QtWidgets import QApplication
from storage.credentials import load_api_key
from gui.login_window import LoginWindow
from gui.main_window import MainWindow


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)

        self.window = None
        self.start()

    def start(self):
        api_key = load_api_key()
        if api_key:
            self.open_main(api_key)
        else:
            self.open_login()

    def open_login(self):
        self.window = LoginWindow(open_main_callback=self.open_main)
        self.window.show()

    def open_main(self, api_key: str):
        if self.window:
            self.window.close()
        self.window = MainWindow(api_key, open_login_callback=self.open_login, recreate_callback=self.recreate_main)
        self.window.show()

    def recreate_main(self, api_key: str):
        self.open_main(api_key)

    def run(self):
        with self.loop:
            self.loop.run_forever()


if __name__ == "__main__":
    AppController().run()
