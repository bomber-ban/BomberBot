# /home/xty/Documents/Projects/PetProject/BomberBot_GUI/BomberBot_GUI/gui/main_window.py

from PySide6.QtWidgets import QMainWindow, QFrame
from api.client import APIClient
from qasync import asyncSlot
from storage.credentials import clear_api_key
import asyncio
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

from .animation import AnimatedButton
from .widgets import Footer, StepWidget, StatusDot, Breadcrumb
from .utils import resource_path


class MainWindow(QMainWindow):
    def __init__(self, api_key: str, open_login_callback, recreate_callback=None):
        super().__init__()

        path = resource_path("gui/styles/main.qss")
        self.load_stylesheet(path)

        self.client = APIClient(api_key)
        self.client.api_key = api_key
        self.open_login_callback = open_login_callback
        self.recreate_callback = recreate_callback

        self.promise_mode = None

        self.breadcrumb = Breadcrumb(go_to_step_callback=self.go_to_step)
        self.setFixedSize(750, 600)
        self.setWindowTitle("BomberBot")

        self.main_layout = QVBoxLayout()

        # Header: Balance + Status + Logout button
        self.main_layout.setSpacing(10)
        header_layout = QHBoxLayout()
        # 1: Balance
        balance_box = QWidget()
        balance_box.setObjectName("header_box")
        balance_box_layout = QHBoxLayout()
        balance_box_layout.setContentsMargins(10, 5, 10, 5)
        balance_box_layout.setAlignment(Qt.AlignCenter)
        self.lbl_balance_label = QLabel("Balance:")
        self.lbl_balance_label.setObjectName("header_text")
        self.lbl_balance = QLabel("---")
        self.lbl_balance.setObjectName("header_text")
        balance_box_layout.addWidget(self.lbl_balance_label)
        balance_box_layout.addWidget(self.lbl_balance)
        balance_box.setLayout(balance_box_layout)

        header_layout.addWidget(balance_box, stretch=1)
        # 2: Status
        status_box = QWidget()
        status_box.setObjectName("header_box")
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(10, 5, 10, 5)
        status_layout.setAlignment(Qt.AlignCenter)

        self.status_dot = StatusDot()
        self.lbl_status_text_label = QLabel("Server status:")
        self.lbl_status_text = QLabel("Unknown")
        self.lbl_status_text_label.setObjectName("header_text")
        self.lbl_status_text.setObjectName("header_text")
        status_layout.addWidget(self.lbl_status_text_label)
        status_layout.addWidget(self.status_dot)
        status_layout.addWidget(self.lbl_status_text)
        status_box.setLayout(status_layout)
        header_layout.addWidget(status_box, stretch=1)
        # 3: Logout button
        logout_box = QWidget()
        logout_box.setObjectName("header_box")
        logout_layout = QHBoxLayout()
        logout_layout.setContentsMargins(10, 5, 10, 5)

        self.logout_btn = AnimatedButton("️Logout", "#1f1f1f", "#8f2115", True)
        self.logout_btn.setObjectName("logout_btn")
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.clicked.connect(self.logout)
        logout_layout.addWidget(self.logout_btn)
        logout_box.setLayout(logout_layout)

        header_layout.addWidget(logout_box, stretch=1)

        self.main_layout.addLayout(header_layout, stretch=0)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(line)

        self.main_layout.addStretch(1)
        # /Header: Balance + Status + Logout button
        # ========================================================================
        # Modes menu

        # Order Title
        self.title_widget = QWidget()
        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 20)
        self.title_layout.setAlignment(Qt.AlignCenter)
        self.title_label = QLabel("Create Order")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title_layout.addWidget(self.title_label)
        self.title_widget.setLayout(self.title_layout)
        self.main_layout.addWidget(self.title_widget)

        # Select regime
        self.mode_widget = QWidget()
        self.mode_layout = QHBoxLayout()
        self.mode_layout.setContentsMargins(45, 0, 45, 0)

        self.btn_mode_smart = AnimatedButton("Smart", "#3498db", "#2980b9")

        self.btn_mode_smart.setCursor(Qt.PointingHandCursor)
        self.btn_mode_smart.setProperty("class", "mode_btn")
        self.btn_mode_smart.clicked.connect(lambda: self.select_mode("Smart"))

        self.btn_mode_time = AnimatedButton("Time", "#3498db", "#2980b9")
        self.btn_mode_time.setCursor(Qt.PointingHandCursor)
        self.btn_mode_time.setProperty("class", "mode_btn")
        self.btn_mode_time.clicked.connect(lambda: self.select_mode("Time"))
        self.mode_layout.addWidget(self.btn_mode_smart)
        self.mode_layout.addWidget(self.btn_mode_time)
        self.mode_layout.setSpacing(20)
        self.mode_widget.setLayout(self.mode_layout)
        self.main_layout.addWidget(self.mode_widget)
        self.main_layout.addWidget(self.breadcrumb)

        # /Select regime

        # Breadcrumbs
        self.modes = {
            "Smart": ["Phone", "Carriers", "Timezone", "Scheduled", "Confirm"],
            "Time": ["Minutes", "Carriers", "Phone", "Scheduled", "Confirm"]
        }
        self.order_data = {
            "Smart": {},
            "Time": {}
        }

        self.current_mode = None
        self.current_step = 0
        self.order_layout = QVBoxLayout()
        self.main_layout.addLayout(self.order_layout)
        self.main_layout.addStretch(1)
        self.footer = Footer()
        self.footer.setAttribute(Qt.WA_StyledBackground, True)
        self.main_layout.addWidget(self.footer)
        # /Breadcrumbs

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
        QTimer.singleShot(0, self.init_async)

    def clear_order_content(self):
        """Clear content between header & footer"""
        self.clear_order_layout()
        self.title_widget.hide()
        self.footer.hide()
        self.main_layout.removeWidget(self.title_widget)
        self.main_layout.removeWidget(self.footer)

        # Hiding breadcrumb
        self.breadcrumb.update_path([], 0)

        # Reset regime
        self.promise_mode = self.current_mode
        self.current_mode = None
        self.current_step = 0

    def load_stylesheet(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def clear_order_layout(self):
        for i in reversed(range(self.order_layout.count())):
            item = self.order_layout.itemAt(i)
            w = item.widget()
            if w:
                self.order_layout.removeWidget(w)
                w.deleteLater()

    def save_step_data(self, step_index, field_name, value):
        mode = self.current_mode
        self.order_data[mode][field_name] = value

    def select_mode(self, mode):
        self.current_mode = mode
        self.current_step = 0
        self.update_ui()

    def update_ui(self):
        # If we do not have selected regime -> hiding form and breadcrumb
        if not self.current_mode:
            self.breadcrumb.update_path([], 0)
            self.clear_order_layout()
            self.mode_widget.show()
            return

        self.mode_widget.hide()
        steps = self.modes[self.current_mode]
        self.breadcrumb.update_path(steps, self.current_step)
        self.load_step_widget(self.current_step)

    def next_step(self):
        steps_count = len(self.modes[self.current_mode])
        if self.current_step < steps_count - 1:
            self.current_step += 1
            self.update_ui()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_ui()

    def go_to_step(self, index):
        if index <= self.current_step:
            self.current_step = index
            self.update_ui()

    def load_step_widget(self, step_index):
        for i in reversed(range(self.order_layout.count())):
            item = self.order_layout.itemAt(i)
            w = item.widget()
            if w:
                self.order_layout.removeWidget(w)
                w.deleteLater()

        mode = self.current_mode
        step_name = self.modes[mode][step_index]
        value = self.order_data[mode].get(step_name, "")

        def submit(value):
            self.save_step_data(step_index, step_name, value)
            self.next_step()

        def cancel():
            # Cancel regime, return to regime selection
            self.promise_mode = self.current_mode
            self.current_mode = None

            self.current_step = 0
            self.order_layout.update()
            self.adjustSize()
            self.update_ui()

        step_widget = StepWidget(step_name, value, submit, cancel, self)
        self.order_layout.addWidget(step_widget)

    @asyncSlot()
    async def init_async(self):
        await self.update_all()

    def reset_main_window(self):
        self.clear_order_content()
        self.update_ui()

    async def update_all(self):
        await self.update_balance()
        await self.update_status()

    async def update_balance(self):
        res = await self.client.fetch_balance()
        bal = res.get("balance", "???")
        self.lbl_balance.setStyleSheet("font-weight: bold;")
        self.lbl_balance.setText(f"{bal}€")

    async def update_status(self):
        res = await self.client.fetch_status()
        status = res.get("status", "").lower()

        if status == "online":
            self.status_dot.set_green()
            self.lbl_status_text.setStyleSheet("font-weight: bold;")
            self.lbl_status_text.setText("Connected")
        else:
            self.status_dot.set_red()
            self.lbl_status_text.setStyleSheet("font-weight: bold;")
            self.lbl_status_text.setText(f"{status}")

    def logout(self):
        clear_api_key()
        self.open_login_callback()
        self.close()



