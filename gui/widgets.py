# /home/xty/Documents/Projects/PetProject/BomberBot_GUI/BomberBot_GUI/gui/widgets.py
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
import json
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPlainTextEdit, QVBoxLayout, QMainWindow, QLineEdit
import traceback
import datetime
from PySide6.QtGui import QMovie
import asyncio
from .animation import AnimatedButton
from .utils import resource_path


class StatusDot(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(12, 12))

    def set_green(self):
        from gui.styles.styles import GREEN_DOT
        self.setStyleSheet(GREEN_DOT)

    def set_red(self):
        from gui.styles.styles import RED_DOT
        self.setStyleSheet(RED_DOT)


class Breadcrumb(QWidget):
    def __init__(self, go_to_step_callback=None):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(40, 5, 5, 5)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)
        self.go_to_step_callback = go_to_step_callback

    def update_path(self, steps: list, current_index: int):
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            w = item.widget()
            if w:
                self.layout.removeWidget(w)
                w.deleteLater()

        for i, step in enumerate(steps):
            label = QLabel(step)
            label.setStyleSheet(
                "color: #3498db; font-size: 17px; font-weight: bold;" if i == current_index else "color: #777;"
            )

            if i < current_index and self.go_to_step_callback:
                label.setCursor(Qt.PointingHandCursor)
                label.mousePressEvent = lambda _, idx=i: self.go_to_step_callback(idx)

            self.layout.addWidget(label)

            if i < len(steps) - 1:
                sep = QLabel(">")
                sep.setStyleSheet("color: #aaa; font-size: 17px; font-weight: bold;")
                sep.setAlignment(Qt.AlignCenter)
                self.layout.addWidget(sep)


class Footer(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("footer")
        self.apply_styles()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(20)

        lbl_github = QLabel()
        lbl_github.setText('<a style="color:#4a4848; text-decoration: none;"'
                           'href="https://github.com/aocoac/BomberBot">GitHub</a>')
        lbl_github.setObjectName("footer_link")
        lbl_github.setOpenExternalLinks(True)

        lbl_site = QLabel()
        lbl_site.setText('<a style="color:#4a4848; text-decoration: none;"'
                         'href="https://bomberbot.cc">BomberBot</a>')
        lbl_site.setObjectName("footer_link")
        lbl_site.setOpenExternalLinks(True)

        now = datetime.datetime.now()
        year = now.year
        lbl_project = QLabel(f"© {year} — BomberBot")
        lbl_project.setObjectName("footer_project")

        layout.addWidget(lbl_github)
        layout.addWidget(lbl_site)
        layout.addStretch()
        layout.addWidget(lbl_project)

    def apply_styles(self):
        try:
            path = resource_path("gui/styles/footer.qss")
            with open(path, "r") as f:
                css = f.read()
                self.setStyleSheet(css)
        except Exception as e:
            print("Failed to load footer styles:", e, traceback.format_exc())


class ApproveWidget(QWidget):
    def __init__(self, step_widget=None):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.btn_approve = AnimatedButton("Approve", "#69d66e", "#4caf50")
        self.layout.addWidget(self.btn_approve)
        self.step_widget = step_widget
        self.btn_approve.clicked.connect(self.on_approve)
        self.process_gif = None
        self.loading_label = None
        self.gif_container = None

    def show_loading(self, gif_path):
        self.gif_container = QWidget()

        process_layout = QVBoxLayout(self.gif_container)
        process_layout.setAlignment(Qt.AlignCenter)
        process_layout.setSpacing(15)

        self.loading_label = QLabel()
        self.loading_label.setFixedSize(256, 256)
        self.loading_label.setScaledContents(True)
        self.process_gif = QMovie(gif_path)
        self.loading_label.setMovie(self.process_gif)

        self.headline = QLabel("Waiting...")
        self.headline.setStyleSheet("font-size: 20px; font-weight: bold;")
        process_layout.addWidget(self.headline, alignment=Qt.AlignCenter)
        process_layout.addWidget(self.loading_label)

        self.process_gif.start()
        self.step_widget.main.main_layout.insertStretch(2, 1)
        self.step_widget.main.main_layout.insertWidget(3, self.gif_container, alignment=Qt.AlignCenter)
        self.step_widget.main.main_layout.insertStretch(4, 1)
        self.footer = Footer()
        self.footer.setAttribute(Qt.WA_StyledBackground, True)
        self.step_widget.main.main_layout.addWidget(self.footer)

    def show_good(self, gif_path, api_response):
        self.gif_good_container = QWidget()

        good_layout = QVBoxLayout(self.gif_good_container)
        good_layout.setAlignment(Qt.AlignCenter)
        good_layout.setSpacing(15)

        self.good_ans_label = QLabel()
        self.good_ans_label.setFixedSize(256, 256)
        self.good_ans_label.setScaledContents(True)

        self.response_box = QPlainTextEdit()
        self.response_box.setReadOnly(True)
        self.response_box.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.response_box.setPlainText(json.dumps(api_response, indent=2))

        self.good_gif = QMovie(gif_path)
        self.good_ans_label.setMovie(self.good_gif)
        self.back_button = AnimatedButton("Back to menu", "#3498db", "#2980b9")

        self.headline_good = QLabel("Success")
        self.headline_good.setStyleSheet("font-size: 20px; font-weight: bold;")
        good_layout.addWidget(self.headline_good, alignment=Qt.AlignCenter)
        good_layout.addWidget(self.good_ans_label)
        good_layout.addWidget(self.response_box)
        good_layout.addWidget(self.back_button)

        self.good_gif.start()
        self.step_widget.main.main_layout.insertStretch(2, 1)
        self.step_widget.main.main_layout.insertWidget(3, self.gif_good_container, alignment=Qt.AlignCenter)
        self.step_widget.main.main_layout.insertStretch(4, 1)

    def show_bad(self, gif_path, api_response):
        self.gif_bad_container = QWidget()

        bad_layout = QVBoxLayout(self.gif_bad_container)
        bad_layout.setAlignment(Qt.AlignCenter)
        bad_layout.setSpacing(15)
        self.bad_ans_label = QLabel()
        self.bad_ans_label.setFixedSize(256, 256)
        self.bad_ans_label.setScaledContents(True)

        self.response_box = QPlainTextEdit()
        self.response_box.setReadOnly(True)
        self.response_box.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.response_box.setPlainText(json.dumps(api_response, indent=2))

        self.bad_gif = QMovie(gif_path)
        self.bad_ans_label.setMovie(self.bad_gif)
        self.back_button = AnimatedButton("Back to menu", "#3498db", "#2980b9")

        self.headline_bad = QLabel("Failure")
        self.headline_bad.setStyleSheet("font-size: 20px; font-weight: bold;")
        bad_layout.addWidget(self.headline_bad, alignment=Qt.AlignCenter)
        bad_layout.addWidget(self.bad_ans_label)
        bad_layout.addWidget(self.response_box)
        bad_layout.addWidget(self.back_button)

        self.bad_gif.start()
        self.step_widget.main.main_layout.insertStretch(2, 1)
        self.step_widget.main.main_layout.insertWidget(3, self.gif_bad_container, alignment=Qt.AlignCenter)
        self.step_widget.main.main_layout.insertStretch(4, 1)

    def clear_main_window_layout(self):
        if self.step_widget.main:
            self.step_widget.main.clear_order_content()
            self.step_widget.main.clear_order_layout()

    def on_approve(self):
        self.clear_main_window_layout()
        path = resource_path("gui/gifs/process.gif")
        self.show_loading(path)
        asyncio.create_task(self.handle_approve())

    def hide_loading(self):
        if getattr(self, "process_gif", None) is not None:
            self.process_gif.stop()
            self.gif_container.hide()
            self.gif_container.setParent(None)
            self.gif_container.deleteLater()
            self.gif_container = None
            self.process_gif = None
            self.clear_layout(self.step_widget.main.main_layout)

    def hide_good(self):
        if getattr(self, "good_gif", None) is not None:
            self.good_gif.stop()

            main_window = self.step_widget.main
            api_key = main_window.client.api_key
            recreate_callback = main_window.recreate_callback

            self.gif_good_container.hide()
            self.gif_good_container.setParent(None)
            self.gif_good_container.deleteLater()
            self.gif_good_container = None
            self.good_gif = None

            main_window.close()

            if recreate_callback:
                recreate_callback(api_key)

    def hide_bad(self):
        if getattr(self, "bad_gif", None) is not None:
            self.bad_gif.stop()

            main_window = self.step_widget.main
            api_key = main_window.client.api_key
            recreate_callback = main_window.recreate_callback

            self.gif_bad_container.hide()
            self.gif_bad_container.setParent(None)
            self.gif_bad_container.deleteLater()
            self.gif_bad_container = None
            self.bad_gif = None

            main_window.close()

            if recreate_callback:
                recreate_callback(api_key)

    async def api_call(self, order_mode, order_details):

        if order_mode == 'Smart':
            if 'Scheduled' in order_details.keys():

                if order_details.get('Scheduled'):

                    api_answer = await self.step_widget.main.client.create_order_scheduled_mode_smart(
                        order_details.get('Phone'), order_details.get('Timezone'), order_details.get('Scheduled')
                    )
                    return api_answer

                else:

                    api_answer = await self.step_widget.main.client.create_order_now_mode_smart(
                        order_details.get('Phone'), order_details.get('Timezone')
                    )
                    return api_answer

        if order_mode == 'Time':
            if 'Scheduled' in order_details.keys():

                if order_details.get('Scheduled'):

                    api_answer = await self.step_widget.main.client.create_order_scheduled_mode_time(
                        order_details.get('Phone'), order_details.get('Minutes'), order_details.get('Scheduled')
                    )
                    return api_answer

                else:

                    api_answer = await self.step_widget.main.client.create_order_now_mode_time(
                        order_details.get('Phone'), order_details.get('Minutes')
                    )
                    return api_answer

    @staticmethod
    def clear_layout(layout):
        i = layout.count() - 1
        while i >= 0:
            item = layout.itemAt(i)
            if item.spacerItem():
                layout.takeAt(i)
            i -= 1

    async def handle_approve(self):
        try:
            order_mode = self.step_widget.main.promise_mode
            order_details = self.step_widget.main.order_data[order_mode]

            api_response = await self.api_call(order_mode, order_details)

            await asyncio.sleep(0.67)
            while not api_response:
                await asyncio.sleep(0.25)

            self.hide_loading()
            self.clear_main_window_layout()

            if api_response.get('detail') == 'Success':
                path = resource_path("gui/gifs/good_answer.gif")
                self.show_good(path, api_response)
                self.back_button.clicked.connect(self.hide_good)
            else:
                path = resource_path("gui/gifs/bad_answer.gif")
                self.show_bad(path, api_response)
                self.back_button.clicked.connect(self.hide_bad)

        except Exception as e:
            await asyncio.sleep(2)
            self.hide_loading()
            self.clear_main_window_layout()
            path = resource_path("gui/gifs/bad_answer.gif")
            self.show_bad(path, {'detail': 'error', 'code': str(e), 'trace': traceback.format_exc()})
            self.back_button.clicked.connect(self.hide_bad)


class StepWidget(QWidget):
    def __init__(self, step_name: str, value: str, submit_callback, cancel_callback, main: QMainWindow):
        super().__init__()
        self.layout = QVBoxLayout()
        self.main = main
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        data = self.main.order_data[self.main.current_mode]

        if self.main.current_mode == 'Smart':
            descriptions = {
                "Phone": "💁🏼‍♀️ In this mode, the number of calls changes dynamically from hour to hour depending\n"
                         "on many factors\n\n"
                         "⏳ Task duration: 2 days\n"
                         "📞 Number of calls: 160\n"
                         "📦 Price of the service: 8 Euros\n"
                         "📌 Each call is unique and comes from a new number",
                "Timezone": "🌎 To continue, please enter the number owner's time zone (from -12 to +12)",
                "Scheduled": "⏰ To continue, send in the chat the date when work on the phone should begin,\n"
                             " or leave the field empty.\n\n"
                             "❗️ For the start, the time will be taken in the UTC format.\n"
                             "⌚️ Current UTC (+0 hours) time on the server and an example of the format:\n\n"
                             f"{datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M')}"
                             f" (UTC timezone)",
                "Confirm": f"📞 Phone: {data.get('Phone')}\n"
                           f"🕘 Task duration: 2 days\n"
                           f"#️⃣ Number of calls/minutes: 160\n"
                           f"💶 Order price: 8.00 Euros\n"
                           f"🌎 Subscriber's time zone: {data.get('Timezone')}\n\n"

                           f"⌚️ The order will start: "
                           f"{data.get('Scheduled') if data.get('Scheduled') else 'NOW'}"

            }
        else:
            descriptions = {
                "Minutes": """📞 Price per call: 0.05 Euro
📌 Each call is unique and comes from a new number
⌨️ Enter how many minutes we should work on this phone""",
                "Phone": "⌨️ To continue, enter your phone number in the field",
                "Scheduled": "⏰ To continue, send in the chat the date when work on the phone should begin,\n"
                             " or leave the field empty.\n\n"
                             "❗️ For the start, the time will be taken in the UTC format.\n"
                             "⌚️ Current UTC (+0 hours) time on the server and an example of the format:\n\n"
                             f"{datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M')}"
                             f" (UTC timezone)",
                "Confirm": f"📞 Phone: {data.get('Phone')}\n"
                           f"🕘 Task duration: {data.get('Minutes')} minutes\n"
                           f"#️⃣ Number of calls/minutes: {data.get('Minutes')}\n"
                           f"💶 Order price: {round(float(data.get('Minutes')) * 0.05, 2) if data.get('Minutes') else 0}"
                           f" Euros\n\n"

                           f"⌚️ The order will start: "
                           f"{data.get('Scheduled') if data.get('Scheduled') else 'NOW'}"
            }

        step_desc = QLabel(descriptions.get(step_name))
        step_desc.setStyleSheet("padding-left: 5px; padding-top: 5px; margin-bottom: 5px; margin-top: 5px;"
                                "color: #aaa; font-size: 18px; font-family: 'Segoe UI', sans-serif")

        layout_desc = QHBoxLayout()
        layout_desc.setContentsMargins(0, 0, 0, 0)
        layout_desc.addWidget(step_desc)
        if step_name == 'Confirm':
            btn_layout = QHBoxLayout()
            self.approve_widget = ApproveWidget(step_widget=self)
            btn_layout.addWidget(self.approve_widget)

            btn_layout.setContentsMargins(5, 5, 5, 5)
            btn_layout.setSpacing(5)

            self.btn_cancel = AnimatedButton("Cancel", "#3498db", "#2980b9")
            # 3498db #2980b9 #1f6391 # logout: #9c3b3b #8f2115
            self.btn_cancel.setCursor(Qt.PointingHandCursor)
            self.btn_cancel.clicked.connect(cancel_callback)

            btn_layout.addWidget(self.btn_cancel)

            self.layout.addLayout(layout_desc)
            self.layout.addLayout(btn_layout)

        else:
            self.layout.addLayout(layout_desc)
            self.input_field = QLineEdit()

            if value:
                self.input_field.setText(value)

            self.input_field.setPlaceholderText(step_name)
            self.input_field.setContentsMargins(5, 5, 5, 5)
            self.layout.addWidget(self.input_field)

            btn_layout = QHBoxLayout()

            self.btn_next = AnimatedButton("Next", "#3498db", "#2980b9")
            self.btn_next.setCursor(Qt.PointingHandCursor)
            btn_layout.setContentsMargins(5, 5, 5, 5)
            btn_layout.setSpacing(15)
            self.btn_next.clicked.connect(lambda: self.go_next(submit_callback))

            self.btn_cancel = AnimatedButton("Cancel", "#3498db", "#2980b9")
            self.btn_cancel.setCursor(Qt.PointingHandCursor)
            self.btn_cancel.clicked.connect(cancel_callback)
            btn_layout.addWidget(self.btn_next)
            btn_layout.addWidget(self.btn_cancel)
            self.layout.addLayout(btn_layout)

            self.error_label = QLabel("")
            self.error_label.setStyleSheet("color: #ff6b6b; font-size: 17px;")
            self.error_label.setAlignment(Qt.AlignCenter)
            self.error_label.hide()
            self.layout.addWidget(self.error_label)

    def go_next(self, submit_callback):
        if not self.validate():
            return
        else:
            submit_callback(self.input_field.text())

    def validate(self):
        try:
            step = self.main.modes[self.main.current_mode][self.main.current_step]
            value = self.input_field.text().strip()
            error = None

            # === PHONE VALIDATION ===
            if step == "Phone":
                if not value.isdigit():
                    error = "Phone number must contain only digits."
                elif len(value) < 9:
                    error = "Phone number is too short."
                elif len(value) > 14:
                    error = "Phone number is too long."
                if not value:
                    error = "Enter the Phone number."

            # === TIMEZONE VALIDATION ===
            elif step == "Timezone":
                try:
                    tz = int(value)
                    if tz < -12 or tz > 12:
                        error = "Timezone must be between -12 and +12."
                except:
                    error = "Timezone must be a number, e.g., -3 or 5."

            # === TIMEZONE VALIDATION ===
            elif step == "Minutes":
                try:
                    minutes = int(value)
                    if minutes < 60 or minutes > 43200:
                        raise RuntimeError
                except RuntimeError:
                    error = "The minimum order is 60 minutes, maximum is 43200 minutes."
                except ValueError:
                    error = "Enter numbers only."

            # === SCHEDULED DATE ===
            elif step == "Scheduled":
                if value:
                    try:
                        _ = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M")
                        _ = _.replace(tzinfo=datetime.timezone.utc)
                        if _ < datetime.datetime.now(datetime.timezone.utc):
                            raise EOFError
                    except EOFError:
                        error = "Date cannot be in the past."
                    except ValueError:
                        error = "Use format YYYY-MM-DD HH:MM."

            # === RESULT OUTPUT ===
            if error:
                self.error_label.setText(error)
                self.error_label.show()
                return False
            else:
                self.error_label.hide()
                return True
        except Exception as e:
            pass


