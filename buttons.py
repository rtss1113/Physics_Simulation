from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QTransform, QPainter, QColor
from PyQt5.QtCore import Qt

from cannon import load_autocropped


def load_horizontal(image_path, height):
    pixmap = load_autocropped(image_path)
    if pixmap.isNull():
        return pixmap
    rotated = pixmap.transformed(QTransform().rotate(90), Qt.SmoothTransformation)
    return rotated.scaledToHeight(height, Qt.SmoothTransformation)


def darkened(pixmap):
    result = pixmap.copy()
    painter = QPainter(result)
    painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
    painter.fillRect(result.rect(), QColor(0, 0, 0, 70))
    painter.end()
    return result


class ImageHoverButton(QPushButton):
    def __init__(self, parent, normal_pixmap, hover_pixmap):
        super().__init__(parent)

        self._normal_pixmap = normal_pixmap
        self._hover_pixmap = hover_pixmap

        self.setIcon(QIcon(self._normal_pixmap))
        self.setIconSize(self._normal_pixmap.size())
        self.setFixedSize(self._normal_pixmap.width() + 6, self._normal_pixmap.height() + 6)
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

    def enterEvent(self, event):
        if not self._hover_pixmap.isNull():
            self.setIcon(QIcon(self._hover_pixmap))
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self._normal_pixmap.isNull():
            self.setIcon(QIcon(self._normal_pixmap))
        super().leaveEvent(event)


class FireButton(ImageHoverButton):
    def __init__(self, parent=None, image_path="assets/white fire button.png", height=50):
        normal_pixmap = load_horizontal(image_path, height)
        hover_pixmap = darkened(normal_pixmap) if not normal_pixmap.isNull() else normal_pixmap
        super().__init__(parent, normal_pixmap, hover_pixmap)


class ResetButton(ImageHoverButton):
    def __init__(self, parent=None,
                 normal_image_path="assets/resetlightgrey.png",
                 hover_image_path="assets/resetdarkgrey.png",
                 height=50):
        normal_pixmap = load_autocropped(normal_image_path).scaledToHeight(height, Qt.SmoothTransformation)
        hover_pixmap = load_autocropped(hover_image_path).scaledToHeight(height, Qt.SmoothTransformation)
        super().__init__(parent, normal_pixmap, hover_pixmap)


class SlowDownButton(ImageHoverButton):
    def __init__(self, parent=None,
                 normal_image_path="assets/going back light grey button.png",
                 hover_image_path="assets/going back dark grey button.png",
                 height=28):
        normal_pixmap = load_autocropped(normal_image_path).scaledToHeight(height, Qt.SmoothTransformation)
        hover_pixmap = load_autocropped(hover_image_path).scaledToHeight(height, Qt.SmoothTransformation)
        super().__init__(parent, normal_pixmap, hover_pixmap)


class SpeedUpButton(ImageHoverButton):
    def __init__(self, parent=None,
                 normal_image_path="assets/speed up light grey button.png",
                 hover_image_path="assets/speed up dark grey button.png",
                 height=28):
        normal_pixmap = load_autocropped(normal_image_path).scaledToHeight(height, Qt.SmoothTransformation)
        hover_pixmap = load_autocropped(hover_image_path).scaledToHeight(height, Qt.SmoothTransformation)
        super().__init__(parent, normal_pixmap, hover_pixmap)