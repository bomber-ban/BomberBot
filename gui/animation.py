# /home/xty/Documents/Projects/PetProject/BomberBot_GUI/BomberBot_GUI/gui/Animation.py
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor


class AnimatedButton(QPushButton):
    def __init__(self, text, from_color, to_color, is_logout=False):
        super().__init__(text)
        self._bg = QColor(from_color)
        self.anim = QPropertyAnimation(self, b"bgColor")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.from_color = from_color
        self.to_color = to_color
        self.is_logout = is_logout
        self.set_bg(self._bg)

    def enterEvent(self, event):
        self.animate_to(QColor(self.to_color))
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_to(QColor(self.from_color))
        return super().leaveEvent(event)

    def animate_to(self, color):
        self.anim.stop()
        self.anim.setStartValue(self._bg)
        self.anim.setEndValue(color)
        self.anim.start()

    def get_bg(self):
        return self._bg

    def set_bg(self, color):
        self._bg = color
        if self.is_logout:
            self.setStyleSheet(f"background-color: {color.name()}; color: white; border-radius: 8px; padding: 6px 10px;")

        else:
            self.setStyleSheet(f"background-color: {color.name()}; color: white; border-radius: 8px; padding: 8px;")

    bgColor = Property(QColor, fget=get_bg, fset=set_bg)