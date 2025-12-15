# /home/xty/Documents/Projects/PetProject/BomberBot_GUI/BomberBot_GUI/gui/login_window.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from storage.credentials import save_api_key
from api.client import APIClient
from PySide6.QtCore import Qt
from .utils import resource_path
from .widgets import AnimatedButton

class LoginWindow(QWidget):
    def __init__(self, open_main_callback):
        super().__init__()
        path = resource_path("gui/styles/login.qss")
        self.load_stylesheet(path)
        self.open_main_callback = open_main_callback
        self.setFixedSize(550, 350)
        self.setWindowTitle("BomberBot")
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(55, 0, 55, 0)

        title = QLabel("Enter to account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.input_key = QLineEdit()
        self.input_key.setPlaceholderText("Enter your API-Key")
        self.input_key.setAlignment(Qt.AlignLeft)
        self.input_key.setEchoMode(QLineEdit.Normal)

        self.btn_login = AnimatedButton("Login", "#3498db", "#2980b9")
        self.btn_login.setFixedHeight(40)
        self.btn_login.clicked.connect(self.login)

        self.lbl_status = QLabel("")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setObjectName("status")

        layout.addWidget(self.input_key)
        layout.addWidget(self.btn_login)

        layout.addWidget(self.lbl_status)
        self.setLayout(layout)

    def load_stylesheet(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    async def login_attempt(self):
        api_key = self.input_key.text().strip()
        if not api_key:
            self.lbl_status.setText("Enter your key.")
            return

        client = APIClient(api_key)
        try:
            res = await client.fetch_balance()
        except:
            self.lbl_status.setText("Connection error.")
            return
        if "balance" in res:
            save_api_key(api_key)
            self.open_main_callback(api_key)
        else:
            self.lbl_status.setText("Wrong key.")

    def login(self):
        import asyncio
        asyncio.create_task(self.login_attempt())
        asyncio.create_task(asyncio.sleep(1.5))
