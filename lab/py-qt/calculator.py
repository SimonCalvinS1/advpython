from math import sqrt

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 320, 470)
        self.setStyleSheet(
            """
            QWidget { background-color: #1f2233; color: white; }
            QLineEdit {
                background-color: purple;
                color: white;
                border: 1px solid black;
                border-radius: 10px;
                padding: 12px;
                font-size: 24px;
            }
            QPushButton {
                background-color: orange;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover { background-color: blue; }
            QPushButton#operator { background-color: red; }
            QPushButton#scientific { background-color: orange; }
            QPushButton#equal { background-color: black; }
            """
        )

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Segoe UI", 20))
        self.layout.addWidget(self.display)

        self.button_grid = QGridLayout()
        self.button_grid.setSpacing(8)
        self.layout.addLayout(self.button_grid)

        self.create_buttons()

    def create_buttons(self):
        button_specs = [
            ("√", self.sqrt_value, "scientific"),
            ("x²", self.square_value, "scientific"),
            ("C", self.clear_display, "operator"),
            ("Undo", self.backspace, "operator"),
            ("7", self.add_to_display),
            ("8", self.add_to_display),
            ("9", self.add_to_display),
            ("/", self.add_to_display),
            ("4", self.add_to_display),
            ("5", self.add_to_display),
            ("6", self.add_to_display),
            ("*", self.add_to_display),
            ("1", self.add_to_display),
            ("2", self.add_to_display),
            ("3", self.add_to_display),
            ("-", self.add_to_display),
            ("0", self.add_to_display),
            (".", self.add_to_display),
            ("+", self.add_to_display),
            ("=", self.calculate_result, "equal"),
        ]

        for index, (text, slot, *extra) in enumerate(button_specs):
            button = QPushButton(text)
            button.setObjectName(extra[0] if extra else "")
            button.clicked.connect(lambda checked, t=text, s=slot: s(t))
            row, col = divmod(index, 4)
            self.button_grid.addWidget(button, row, col)

    def add_to_display(self, text):
        current_text = self.display.text()
        if current_text == "Error":
            current_text = ""
        self.display.setText(current_text + text)

    def clear_display(self, _=None):
        self.display.clear()

    def backspace(self, _=None):
        self.display.setText(self.display.text()[:-1])

    def sqrt_value(self, _=None):
        current_text = self.display.text().strip()
        if not current_text or current_text == "Error":
            return
        try:
            value = float(current_text)
            if value < 0:
                self.display.setText("Error")
            else:
                self.display.setText(str(sqrt(value)))
        except Exception:
            self.display.setText("Error")

    def square_value(self, _=None):
        current_text = self.display.text().strip()
        if not current_text or current_text == "Error":
            return
        try:
            value = float(current_text)
            self.display.setText(str(value * value))
        except Exception:
            self.display.setText("Error")

    def calculate_result(self, _=None):
        current_text = self.display.text().strip()
        if not current_text or current_text == "Error":
            return
        try:
            result = eval(current_text, {"__builtins__": {}}, {})
            self.display.setText(str(result))
        except Exception:
            self.display.setText("Error")


if __name__ == "__main__":
    app = QApplication([])
    calculator = Calculator()
    calculator.show()
    app.exec()