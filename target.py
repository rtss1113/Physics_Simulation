from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from paths import resource_path


class Target(QLabel):

    moved = pyqtSignal(int, int)

    def __init__(self, parent=None, image_path="assets/target.png", size=100, ground_y=None):
        super().__init__(parent)

        pixmap = QPixmap(resource_path(image_path))
        pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.setPixmap(pixmap)
        self.setFixedSize(pixmap.size())
        self.setStyleSheet("background: transparent;")
        self.setCursor(Qt.OpenHandCursor)

        self._dragging = False
        self._drag_offset = QPoint()

        self.ground_y = ground_y

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_offset = event.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self._dragging:
            new_pos = self.mapToParent(event.pos() - self._drag_offset)

            parent = self.parentWidget()
            if parent is not None:
                min_x = 0
                max_x = parent.width() - self.width()
                min_y = 0
                max_y = parent.height() - self.height()

                if self.ground_y is not None:
                    max_y = min(max_y, self.ground_y - self.height())

                new_x = min(max(new_pos.x(), min_x), max_x)
                new_y = min(max(new_pos.y(), min_y), max_y)
                new_pos.setX(new_x)
                new_pos.setY(new_y)
            elif self.ground_y is not None:
                max_y = self.ground_y - self.height()
                if new_pos.y() > max_y:
                    new_pos.setY(max_y)

            self.move(new_pos)
            self.moved.emit(new_pos.x(), new_pos.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            self.setCursor(Qt.OpenHandCursor)

    def moveTo(self, x, y):
        self.move(x, y)
        self.moved.emit(x, y)