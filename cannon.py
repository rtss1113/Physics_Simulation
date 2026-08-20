import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter, QBitmap, QRegion
from PyQt5.QtCore import Qt, QPoint, QPointF, pyqtSignal
from paths import resource_path


def load_autocropped(path):
    full_path = resource_path(path)
    pixmap = QPixmap(full_path)

    image = pixmap.toImage()
    mask = QBitmap.fromImage(image.createAlphaMask())
    region = QRegion(mask)
    rect = region.boundingRect()

    if rect.isValid() and not rect.isEmpty():
        pixmap = pixmap.copy(rect)

    return pixmap


class Cannon(QWidget):
    moved = pyqtSignal(int)
    head_tilt_fix = 11.87
    max_firing_angle = 80

    def __init__(self, parent=None,
                 lift_path="assets/cannonlift&leg.png",
                 head_path="assets/cannonhead.png",
                 lift_height=110, head_height=70,
                 ground_y=None, top_y=0):
        super().__init__(parent)

        raw_lift = load_autocropped(lift_path)
        self.lift_pixmap = raw_lift.scaledToHeight(lift_height, Qt.SmoothTransformation) if not raw_lift.isNull() else raw_lift

        raw_head = load_autocropped(head_path)
        self.head_pixmap = raw_head.scaledToHeight(head_height, Qt.SmoothTransformation) if not raw_head.isNull() else raw_head

        # these ratios were eyeballed against the sprite sheet - the pivot point (where the
        # barrel rotates from) and the muzzle (where the ball actually spawns) aren't in the
        # image metadata anywhere so they just get hardcoded as fractions of the pixmap size
        self.head_pivot_x = int(self.head_pixmap.width() * 0.26)
        self.head_pivot_y = int(self.head_pixmap.height() * 0.66)

        self.head_muzzle_x = int(self.head_pixmap.width() * 1.02)
        self.head_muzzle_y = int(self.head_pixmap.height() * 0.16)

        lift_dot_x = int(self.lift_pixmap.width() * 0.674)
        lift_dot_y = int(self.lift_pixmap.height() * 0.058)

        self.head_offset_x = lift_dot_x - self.head_pivot_x
        self.head_offset_y = lift_dot_y - self.head_pivot_y

        min_x = min(0, self.head_offset_x)
        min_y = min(0, self.head_offset_y)
        max_x = max(self.lift_pixmap.width(), self.head_offset_x + self.head_pixmap.width())
        max_y = max(self.lift_pixmap.height(), self.head_offset_y + self.head_pixmap.height())

        # widget needs to be big enough to contain the head at every rotation, not just angle 0,
        # so work out the farthest any head corner gets from the pivot and pad the bounds by that
        pivot_x = self.head_offset_x + self.head_pivot_x
        pivot_y = self.head_offset_y + self.head_pivot_y
        corners = [
            (self.head_offset_x, self.head_offset_y),
            (self.head_offset_x + self.head_pixmap.width(), self.head_offset_y),
            (self.head_offset_x, self.head_offset_y + self.head_pixmap.height()),
            (self.head_offset_x + self.head_pixmap.width(), self.head_offset_y + self.head_pixmap.height()),
        ]
        sweep_radius = max(math.hypot(cx - pivot_x, cy - pivot_y) for cx, cy in corners)

        min_x = math.floor(min(min_x, pivot_x - sweep_radius))
        min_y = math.floor(min(min_y, pivot_y - sweep_radius))
        max_x = math.ceil(max(max_x, pivot_x + sweep_radius))
        max_y = math.ceil(max(max_y, pivot_y + sweep_radius))

        self._lift_draw_pos = QPoint(-min_x, -min_y)
        self._head_draw_pos = QPoint(self.head_offset_x - min_x, self.head_offset_y - min_y)
        self._head_pivot = QPointF(
            self._head_draw_pos.x() + self.head_pivot_x,
            self._head_draw_pos.y() + self.head_pivot_y
        )

        self.lift_bottom_offset = self._lift_draw_pos.y() + self.lift_pixmap.height()

        width = max(1, max_x - min_x)
        height = max(1, max_y - min_y)
        self.setFixedSize(width, height)
        self.setCursor(Qt.OpenHandCursor)

        self._dragging = False
        self._drag_start_y = 0
        self._widget_start_y = 0

        self.ground_y = ground_y
        self.top_y = top_y

        self.firing_angle = 0

    def set_firing_angle(self, angle_deg):
        angle_deg = max(0, min(angle_deg, self.max_firing_angle))
        self.firing_angle = angle_deg
        self.update()

    def muzzle_point(self):
        # rotate the muzzle point around the pivot by the same angle paintEvent rotates the sprite,
        # otherwise the cannonball spawns from wherever the muzzle sits at angle 0 every time
        angle = math.radians(self.head_tilt_fix - self.firing_angle)
        dx = self.head_muzzle_x - self.head_pivot_x
        dy = self.head_muzzle_y - self.head_pivot_y
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        local_x = self._head_pivot.x() + dx * cos_a - dy * sin_a
        local_y = self._head_pivot.y() + dx * sin_a + dy * cos_a
        return QPoint(self.x() + int(local_x), self.y() + int(local_y))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        if not self.lift_pixmap.isNull():
            painter.drawPixmap(self._lift_draw_pos, self.lift_pixmap)

        if not self.head_pixmap.isNull():
            painter.save()
            painter.translate(self._head_pivot)
            painter.rotate(self.head_tilt_fix - self.firing_angle)
            painter.translate(-self._head_pivot)
            painter.drawPixmap(self._head_draw_pos, self.head_pixmap)
            painter.restore()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_start_y = event.globalY()
            self._widget_start_y = self.y()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self._dragging:
            delta_y = event.globalY() - self._drag_start_y
            new_y = self._widget_start_y + delta_y

            if self.top_y is not None:
                new_y = max(new_y, self.top_y)
            if self.ground_y is not None:
                new_y = min(new_y, self.ground_y - self.lift_bottom_offset)

            self.move(self.x(), new_y)
            self.moved.emit(new_y)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            self.setCursor(Qt.OpenHandCursor)

    def moveTo(self, y):
        if self.top_y is not None:
            y = max(y, self.top_y)
        if self.ground_y is not None:
            y = min(y, self.ground_y - self.lift_bottom_offset)
        self.move(self.x(), y)
        self.moved.emit(y)