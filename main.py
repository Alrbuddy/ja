import sys
from PyQt5.QtCore import QTimer, Qt, QSettings, QDateTime, QTime, QDate
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QColor, QPalette

colors = [
    Qt.red,
    Qt.darkRed,
    Qt.green,
    Qt.darkGreen,
    Qt.blue,
    Qt.darkBlue,
    Qt.cyan,
    Qt.darkCyan,
    Qt.magenta,
    Qt.darkMagenta,
    Qt.yellow,
    Qt.darkYellow
]

current_color_index = 0

def change_color():
    global current_color_index
    palette = window.palette()
    palette.setColor(QPalette.Background, colors[current_color_index])
    window.setPalette(palette)
    current_color_index = (current_color_index + 1) % len(colors)

def restart_timer():
    global current_color_index
    current_color_index = 0
    change_color()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Animation Spoofer")
window.setGeometry(100, 100, 400, 300)

countdown_label = QLabel("Down for maintenance, Estimated time: 8-9 Days, On vacation.")
countdown_label.setAlignment(Qt.AlignCenter)

layout = QVBoxLayout()
layout.addWidget(countdown_label)

window.setLayout(layout)

countdown_timer = QTimer()
countdown_timer.timeout.connect(change_color)
countdown_timer.start(1000)

window.show()
sys.exit(app.exec_())
