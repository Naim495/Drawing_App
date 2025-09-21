# main.py
# Run: pip install PyQt5
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QColorDialog,
    QSlider, QLabel, QHBoxLayout, QVBoxLayout, QComboBox, QTabWidget
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint

# 🎨 Canvas Class
class Canvas(QWidget):
    def __init__(self, width=800, height=600):
        super().__init__()
        self.setFixedSize(width, height)
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(Qt.transparent)  # লেয়ার ব্যাকগ্রাউন্ড স্বচ্ছ

        self.last_point = None
        self.brush_color = QColor("black")
        self.brush_size = 5
        self.brush_type = "Pencil"  # ডিফল্ট ব্রাশ

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)  # ব্যাকগ্রাউন্ড সাদা
        painter.drawPixmap(0, 0, self.pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()
            self.draw_line(self.last_point, self.last_point)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.last_point:
            current = event.pos()
            self.draw_line(self.last_point, current)
            self.last_point = current

    def mouseReleaseEvent(self, event):
        self.last_point = None

    def draw_line(self, p1: QPoint, p2: QPoint):
        painter = QPainter(self.pixmap)

        # ✏️ Brush Styles with Alpha
        if self.brush_type == "Pencil":
            color = QColor(self.brush_color)
            color.setAlpha(120)  # হালকা শেড
            pen = QPen(color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        elif self.brush_type == "Ink Pen":
            color = QColor(self.brush_color)
            color.setAlpha(200)  # একটু গাঢ়
            pen = QPen(color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        elif self.brush_type == "Ball Pen":
            color = QColor(self.brush_color)
            color.setAlpha(255)  # পুরো গাঢ়
            pen = QPen(color, self.brush_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        elif self.brush_type == "Brush":
            color = QColor(self.brush_color)
            color.setAlpha(80)   # অনেক হালকা
            pen = QPen(color, self.brush_size * 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        else:
            pen = QPen(self.brush_color, self.brush_size)

        painter.setPen(pen)
        painter.drawLine(p1, p2)
        self.update()

    def clear(self):
        self.pixmap.fill(Qt.transparent)
        self.update()


# 🖥️ Main Window with Layers
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procreate-like Drawing App (Python)")

        # Tabs for Layers
        self.layers = QTabWidget()
        self.add_layer("Layer 1")

        # Brush Options
        brush_label = QLabel("Brush:")
        self.brush_combo = QComboBox()
        self.brush_combo.addItems(["Pencil", "Ink Pen", "Ball Pen", "Brush"])
        self.brush_combo.currentTextChanged.connect(self.change_brush)

        # Brush Size
        size_label = QLabel("Size:")
        size_slider = QSlider(Qt.Horizontal)
        size_slider.setRange(1, 50)
        size_slider.setValue(5)
        size_slider.valueChanged.connect(self.change_brush_size)

        # Color Picker
        color_btn = QPushButton("Color")
        color_btn.clicked.connect(self.choose_color)

        # Clear Button
        clear_btn = QPushButton("Clear Layer")
        clear_btn.clicked.connect(self.clear_layer)

        # Add Layer Button
        add_layer_btn = QPushButton("➕ Add Layer")
        add_layer_btn.clicked.connect(self.new_layer)

        # Layouts
        top_layout = QHBoxLayout()
        top_layout.addWidget(brush_label)
        top_layout.addWidget(self.brush_combo)
        top_layout.addWidget(size_label)
        top_layout.addWidget(size_slider)
        top_layout.addWidget(color_btn)
        top_layout.addWidget(clear_btn)
        top_layout.addWidget(add_layer_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.layers)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.resize(900, 700)

    # 🟢 Layer Functions
    def add_layer(self, name):
        canvas = Canvas()
        self.layers.addTab(canvas, name)

    def new_layer(self):
        count = self.layers.count() + 1
        self.add_layer(f"Layer {count}")

    def current_canvas(self):
        return self.layers.currentWidget()

    def clear_layer(self):
        canvas = self.current_canvas()
        if canvas:
            canvas.clear()

    # 🟢 Brush Functions
    def change_brush(self, brush_name):
        canvas = self.current_canvas()
        if canvas:
            canvas.brush_type = brush_name

    def change_brush_size(self, size):
        canvas = self.current_canvas()
        if canvas:
            canvas.brush_size = size

    def choose_color(self):
        canvas = self.current_canvas()
        if canvas:
            col = QColorDialog.getColor(canvas.brush_color, self, "Choose Brush Color")
            if col.isValid():
                canvas.brush_color = col


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
