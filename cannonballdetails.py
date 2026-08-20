from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class CannonballDetails(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window, Qt.Window)
        self.main_window = main_window
        self.setWindowTitle("Cannonball Details")
        self.setFixedSize(600, 400)
        self.setStyleSheet("font-size: 13px;")


        cannonball_title_label = QLabel("Cannonball Details")
        self.cannonball_mass_info = QLabel("Cannonball Mass:__kg")
        self.cannonball_radius_info = QLabel("Cannonball Radius:__cm")

        v_title_label = QLabel("Velocity")
        self.v_hori_info = QLabel("v<sub>horizontal</sub>:__m/s<sup>1</sup>")
        self.v_vert_info = QLabel("v<sub>vertical</sub>:__m/s<sup>1</sup>")
        self.v_total_info = QLabel("v<sub>total</sub>:__m/s<sup>1</sup>")

        a_title_label = QLabel("Acceleration")
        self.a_hori_info = QLabel("a<sub>horizontal</sub>:__m/s<sup>2</sup>")
        self.a_vert_info = QLabel("a<sub>vertical</sub>:__m/s<sup>2</sup>")
        self.a_total_info = QLabel("a<sub>total</sub>:__m/s<sup>2</sup>")

        e_title_label = QLabel("Energy")
        self.ke_info = QLabel("Kinetic Energy:__j")
        self.gpe_info = QLabel("Gravitational Potential Energy:__j")

        posi_title_label = QLabel("Position")
        self.posi_hori_info = QLabel("Horizontal:__m")
        self.posi_vert_info = QLabel("Vertical:__m")

        layout = QVBoxLayout()

        layout.addStretch()


        row1 = QHBoxLayout()
        row1.addStretch(1)
        row1.addWidget(cannonball_title_label)
        row1.addStretch(3)

        layout.addLayout(row1)
        layout.addWidget(self.cannonball_mass_info, alignment=Qt.AlignHCenter)
        layout.addWidget(self.cannonball_radius_info, alignment=Qt.AlignHCenter)

        row2 = QHBoxLayout()
        row2.addStretch(1)
        row2.addWidget(v_title_label)
        row2.addStretch(3)

        layout.addLayout(row2)
        layout.addWidget(self.v_hori_info, alignment=Qt.AlignHCenter)
        layout.addWidget(self.v_vert_info, alignment=Qt.AlignHCenter)
        layout.addWidget(self.v_total_info, alignment=Qt.AlignHCenter)

        row3 = QHBoxLayout()
        row3.addStretch(1)
        row3.addWidget(a_title_label)
        row3.addStretch(3)

        layout.addLayout(row3)
        layout.addWidget(self.a_hori_info, alignment=Qt.AlignHCenter)
        layout.addWidget(self.a_vert_info, alignment=Qt.AlignHCenter)
        layout.addWidget(self.a_total_info, alignment=Qt.AlignHCenter)


        row4 = QHBoxLayout()
        row4.addStretch(1)
        row4.addWidget(e_title_label)
        row4.addStretch(3)

        layout.addLayout(row4)
        layout.addWidget(self.ke_info, alignment=Qt.AlignHCenter)
        layout.addWidget(self.gpe_info, alignment=Qt.AlignHCenter)

        row5 = QHBoxLayout()
        row5.addStretch(1)
        row5.addWidget(posi_title_label)
        row5.addStretch(3)

        layout.addLayout(row5)
        layout.addWidget(self.posi_hori_info, alignment=Qt.AlignHCenter)
        layout.addWidget(self.posi_vert_info, alignment=Qt.AlignHCenter)

        layout.addStretch()

        self.setLayout(layout)

    def update_display(self):
        mw = self.main_window

        self.cannonball_mass_info.setText(f"Cannonball Mass:{mw.cannonball_mass:.2f}kg")
        self.cannonball_radius_info.setText(f"Cannonball Radius:{mw.cannonball_radius:.2f}cm")

        self.v_hori_info.setText(f"v<sub>horizontal</sub>:{mw.v_horizontal:.2f}m/s<sup>1</sup>")
        self.v_vert_info.setText(f"v<sub>vertical</sub>:{mw.v_vertical:.2f}m/s<sup>1</sup>")
        self.v_total_info.setText(f"v<sub>total</sub>:{mw.v_total:.2f}m/s<sup>1</sup>")

        self.a_hori_info.setText(f"a<sub>horizontal</sub>:{mw.a_horizontal:.2f}m/s<sup>2</sup>")
        self.a_vert_info.setText(f"a<sub>vertical</sub>:{mw.a_vertical:.2f}m/s<sup>2</sup>")
        self.a_total_info.setText(f"a<sub>total</sub>:{mw.a_total:.2f}m/s<sup>2</sup>")

        self.ke_info.setText(f"Kinetic Energy:{mw.kinetic_energy:.2f}j")
        self.gpe_info.setText(f"Gravitational Potential Energy:{mw.gpe:.2f}j")

        self.posi_hori_info.setText(f"Horizontal:{mw.position_horizontal:.2f}m")
        self.posi_vert_info.setText(f"Vertical:{mw.position_vertical:.2f}m")