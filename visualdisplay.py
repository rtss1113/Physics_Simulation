from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class VisualDisplay(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window, Qt.Window)
        self.main_window = main_window
        self.setWindowTitle("Visual Display")
        self.setFixedSize(250, 100)
        self.setStyleSheet("font-family: Arial;")

        acceleration_arrows_label = QLabel("Show Acceleration arrow(Blue)")
        self.acceleration_arrows_checkbox = QCheckBox()
        self.acceleration_arrows_checkbox.setChecked(main_window.show_acceleration_arrows)
        self.acceleration_arrows_checkbox.stateChanged.connect(self.change_show_acceleration_arrows)

        velocity_arrows_label = QLabel("Show Velocity arrow(Red)")
        self.velocity_arrows_checkbox = QCheckBox()
        self.velocity_arrows_checkbox.setChecked(main_window.show_velocity_arrows)
        self.velocity_arrows_checkbox.stateChanged.connect(self.change_show_velocity_arrows)

        layout = QVBoxLayout()

        acceleration_arrows_row = QHBoxLayout()
        acceleration_arrows_row.addWidget(acceleration_arrows_label)
        acceleration_arrows_row.addWidget(self.acceleration_arrows_checkbox)

        layout.addLayout(acceleration_arrows_row)

        velocity_arrows_row = QHBoxLayout()
        velocity_arrows_row.addWidget(velocity_arrows_label)
        velocity_arrows_row.addWidget(self.velocity_arrows_checkbox)

        layout.addLayout(velocity_arrows_row)


        self.setLayout(layout)

    def change_show_acceleration_arrows(self, state):
        self.main_window.change_show_acceleration_arrows(state == Qt.Checked)

    def change_show_velocity_arrows(self, state):
        self.main_window.change_show_velocity_arrows(state == Qt.Checked)