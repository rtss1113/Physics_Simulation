from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtCore import Qt

from cannon import load_autocropped


def darkened(pixmap):
    result = pixmap.copy()
    painter = QPainter(result)
    painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
    painter.fillRect(result.rect(), QColor(0, 0, 0, 70))
    painter.end()
    return result


class PauseResumeButton(QPushButton):
    def __init__(self, parent=None,
                 play_image_path="assets/dark green button.png",
                 pause_image_path="assets/light red button.png",
                 pause_hover_image_path="assets/dark red button.png",
                 height=32):
        super().__init__(parent)

        self.play_normal = load_autocropped(play_image_path).scaledToHeight(height, Qt.SmoothTransformation)
        self._play_hover = darkened(self.play_normal)
        self._pause_normal = load_autocropped(pause_image_path).scaledToHeight(height, Qt.SmoothTransformation)
        self._pause_hover = load_autocropped(pause_hover_image_path).scaledToHeight(height, Qt.SmoothTransformation)

        self.is_playing = False
        self._hovering = False

        self.setFixedSize(self.play_normal.width() + 6, self.play_normal.height() + 6)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:disabled {
                background: rgba(0, 0, 0, 30);
                border-radius: 6px;
            }
        """)
        self.refresh_icon()

    def set_playing_state(self, is_playing):
        self.is_playing = is_playing
        self.refresh_icon()

    def refresh_icon(self):
        if self.is_playing:
            pixmap = self._pause_hover if self._hovering else self._pause_normal
        else:
            pixmap = self._play_hover if self._hovering else self.play_normal
        self.setIcon(QIcon(pixmap))
        self.setIconSize(pixmap.size())

    def enterEvent(self, event):
        self._hovering = True
        self.refresh_icon()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovering = False
        self.refresh_icon()
        super().leaveEvent(event)