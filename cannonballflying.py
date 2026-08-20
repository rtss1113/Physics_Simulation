import math

import pymunk
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QRadialGradient, QPen, QPolygonF
from PyQt5.QtCore import Qt, QTimer, QPointF, pyqtSignal

from constants import DEFAULT_DRAG_COEFFICIENT, STEP_INTERVAL_MS, BASE_SIMULATION_SPEED, CANNONBALL_VISUAL_SCALE


class CannonballPreview(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.radius_m = main_window.cannonball_radius / 100
        self._update_pixel_size()

    def set_radius(self, radius_m):
        self.radius_m = radius_m
        self._update_pixel_size()

    def _update_pixel_size(self):
        diameter_px = max(10, int(self.radius_m * 2 * self.main_window.pixels_per_meter * CANNONBALL_VISUAL_SCALE))
        self.setFixedSize(diameter_px, diameter_px)

    def reposition_at(self, muzzle_point):
        self.move(muzzle_point.x() - self.width() // 2, muzzle_point.y() - self.height() // 2)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QRadialGradient(self.width() * 0.35, self.height() * 0.35, self.width() * 0.9)
        gradient.setColorAt(0, QColor(110, 110, 110))
        gradient.setColorAt(1, QColor(25, 25, 25))

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect())


class VectorArrow(QWidget):
    def __init__(self, parent, color):
        super().__init__(parent)
        self.color = color
        self.start = QPointF(0, 0)
        self.end = QPointF(0, 0)
        self.visible_flag = False
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def set_vector(self, start, end):
        self.start = start
        self.end = end
        self.update()

    def show_arrow(self):
        self.visible_flag = True
        self.update()

    def hide_arrow(self):
        if self.visible_flag:
            self.visible_flag = False
            self.update()

    def paintEvent(self, event):
        if not self.visible_flag:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(self.color, 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(self.start, self.end)

        angle = math.atan2(self.end.y() - self.start.y(), self.end.x() - self.start.x())
        arrow_size = 10
        p2 = QPointF(
            self.end.x() - arrow_size * math.cos(angle - math.pi / 6),
            self.end.y() - arrow_size * math.sin(angle - math.pi / 6)
        )
        p3 = QPointF(
            self.end.x() - arrow_size * math.cos(angle + math.pi / 6),
            self.end.y() - arrow_size * math.sin(angle + math.pi / 6)
        )

        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(QPolygonF([self.end, p2, p3]))


class CannonballFlight(QWidget):
    landed = pyqtSignal()

    def __init__(self, main_window, start_x_m, start_y_m, velocity_x, velocity_y, mass_kg, radius_m):
        super().__init__(main_window)
        self.main_window = main_window

        self.mass = mass_kg
        self.radius_m = radius_m
        self.time_elapsed = 0.0

        self.space = pymunk.Space()
        self.space.gravity = (0, 0)  # gravity handled manually in _velocity_func so drag can be layered on top

        moment = pymunk.moment_for_circle(mass_kg, 0, radius_m)
        self.body = pymunk.Body(mass_kg, moment)
        self.body.position = (start_x_m, start_y_m)
        self.body.velocity = (velocity_x, velocity_y)

        self.shape = pymunk.Circle(self.body, radius_m)
        self.shape.friction = 0.5
        self.space.add(self.body, self.shape)

        self.body.velocity_func = self._velocity_func

        self.last_ax = 0.0
        self.last_ay = -main_window.gravity

        self._update_pixel_size()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._step)

    def _update_pixel_size(self):
        diameter_px = max(10, int(self.radius_m * 2 * self.main_window.pixels_per_meter * CANNONBALL_VISUAL_SCALE))
        self.setFixedSize(diameter_px, diameter_px)

    def _velocity_func(self, body, gravity, damping, dt):
        # overriding pymunk's built in integrator so drag scales with actual speed^2 instead of a flat damping value
        g = self.main_window.gravity

        vx, vy = body.velocity
        speed = math.hypot(vx, vy)

        if self.main_window.air_resistance_enabled:
            air_density = self.main_window.air_density
            area = math.pi * (self.radius_m ** 2)
            drag_force = 0.5 * air_density * DEFAULT_DRAG_COEFFICIENT * area * (speed ** 2)

            if speed > 0:
                drag_ax = -drag_force * (vx / speed) / self.mass
                drag_ay = -drag_force * (vy / speed) / self.mass
            else:
                drag_ax = 0.0
                drag_ay = 0.0
        else:
            drag_ax = 0.0
            drag_ay = 0.0

        ax = drag_ax
        ay = -g + drag_ay

        self.last_ax = ax
        self.last_ay = ay

        body.velocity = (vx + ax * dt, vy + ay * dt)

    def start(self):
        self.timer.start(STEP_INTERVAL_MS)

    def stop(self):
        self.timer.stop()

    def pause(self):
        self.timer.stop()

    def resume(self):
        self.timer.start(STEP_INTERVAL_MS)

    def is_paused(self):
        return not self.timer.isActive()

    def set_state(self, x_m, y_m):
        self._reposition(x_m, y_m)

    def set_full_state(self, x_m, y_m, vx, vy, time_elapsed):
        self.body.position = (x_m, y_m)
        self.body.velocity = (vx, vy)
        self.time_elapsed = time_elapsed
        self._reposition(x_m, y_m)

    def _step(self):
        dt = (STEP_INTERVAL_MS / 1000) * BASE_SIMULATION_SPEED * self.main_window.simulation_speed_multiplier
        self.space.step(dt)
        self.time_elapsed += dt

        x_m, y_m = self.body.position
        vx, vy = self.body.velocity

        ground_level = self.radius_m  # ball center sits one radius above y=0 when resting on the ground
        landed = y_m <= ground_level

        if landed:
            y_m = ground_level
            vx, vy = 0.0, 0.0
            self.body.position = (x_m, y_m)
            self.body.velocity = (0, 0)

        self._reposition(x_m, y_m)
        self.main_window.on_cannonball_physics_update(self.time_elapsed, x_m, y_m, vx, vy, self.last_ax, self.last_ay)

        off_screen = self.x() > self.main_window.width() or self.x() + self.width() < 0
        if landed or off_screen:
            self.timer.stop()
            self.landed.emit()

    def _reposition(self, x_m, y_m):
        mw = self.main_window
        self._update_pixel_size()

        centre_px_x = mw.origin_x + (x_m * mw.pixels_per_meter)
        centre_px_y = mw.origin_y - (y_m * mw.pixels_per_meter)

        self.move(int(centre_px_x - self.width() / 2), int(centre_px_y - self.height() / 2))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QRadialGradient(self.width() * 0.35, self.height() * 0.35, self.width() * 0.9)
        gradient.setColorAt(0, QColor(110, 110, 110))
        gradient.setColorAt(1, QColor(25, 25, 25))

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect())