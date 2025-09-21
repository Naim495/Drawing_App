import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QColorDialog, QListWidget, QSlider, QLabel, QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor
from PyQt5.QtCore import Qt, QPoint


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.layers = []
        self.current_layer = None
        self.last_point = QPoint()
        self.drawing = False

        # Default brush settings
        self.brush_color = QColor(0, 0, 0)
        self.brush_size = 3
        self.brush_type = "Pencil"

        self.add_layer("Background")

    def add_layer(self, name="Layer"):
        layer = QPixmap(self.size())
        layer.fill(Qt.transparent)
        self.layers.append({
            "pixmap": layer,
            "name": name,
            "opacity": 1.0,
            "visible": True
        })
        self.current_layer = self.layers[-1]

    def set_brush_color(self, color):
        self.brush_color = color

    def set_brush_size(self, size):
        self.brush_size = size

    def set_brush_type(self, brush_type):
        self.brush_type = brush_type

    def set_layer_opacity(self, value):
        if self.current_layer:
            self.current_layer["opacity"] = value / 100.0
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.current_layer:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing and self.current_layer:
            painter = QPainter(self.current_layer["pixmap"])
            pen = QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

            # Different brush styles
            if self.brush_type == "Pencil":
                pen.setWidth(1)
            elif self.brush_type == "Ink Pen":
                pen.setWidth(self.brush_size)
            elif self.brush_type == "Ball Pen":
                pen.setWidth(self.brush_size + 1)
            elif self.brush_type == "Brush":
                pen.setWidth(self.brush_size * 2)

            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)  # White background
        for layer in self.layers:
            if layer["visible"]:
                painter.setOpacity(layer["opacity"])
                painter.drawPixmap(0, 0, layer["pixmap"])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procreate Clone in Python")
        self.canvas = Canvas()

        # UI Layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        # Brush options
        brush_layout = QHBoxLayout()
        self.color_btn = QPushButton("Choose Color")
        self.color_btn.clicked.connect(self.choose_color)
        brush_layout.addWidget(self.color_btn)

        self.brush_type_box = QComboBox()
        self.brush_type_box.addItems(["Pencil", "Ink Pen", "Ball Pen", "Brush"])
        self.brush_type_box.currentTextChanged.connect(self.change_brush_type)
        brush_layout.addWidget(QLabel("Brush Type:"))
        brush_layout.addWidget(self.brush_type_box)

        self.brush_size_slider = QSlider(Qt.Horizontal)
        self.brush_size_slider.setRange(1, 20)
        self.brush_size_slider.setValue(3)
        self.brush_size_slider.valueChanged.connect(self.change_brush_size)
        brush_layout.addWidget(QLabel("Brush Size:"))
        brush_layout.addWidget(self.brush_size_slider)

        layout.addLayout(brush_layout)

        # Layer System
        self.layer_list = QListWidget()
        layout.addWidget(QLabel("Layers"))
        layout.addWidget(self.layer_list)

        add_layer_btn = QPushButton("Add Layer")
        add_layer_btn.clicked.connect(self.add_layer)
        layout.addWidget(add_layer_btn)

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.change_opacity)
        layout.addWidget(QLabel("Layer Opacity"))
        layout.addWidget(self.opacity_slider)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.add_layer("Layer 1")

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_brush_color(color)

    def change_brush_type(self, brush_type):
        self.canvas.set_brush_type(brush_type)

    def change_brush_size(self, value):
        self.canvas.set_brush_size(value)

    def add_layer(self, name=None):
        if not name:
            name = f"Layer {len(self.canvas.layers)}"
        self.canvas.add_layer(name)
        self.layer_list.addItem(name)

    def change_opacity(self, value):
        self.canvas.set_layer_opacity(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


