import sys, re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QMessageBox, QVBoxLayout, QHBoxLayout, 
    QFormLayout, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QCloseEvent

class SafeBiteValidationError(Exception):
    pass


class SafeBiteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SafeBite: Allergy Companion")
        self.setMinimumSize(450, 600)
        self.profile_registered = False
        self.user_name = ""
        self.user_allergies = []
        self.severity_level = "Severe"
        self.setMouseTracking(True)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        title_label = QLabel("SafeBite: Dietary Allergy Checker")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 5px;")
        main_layout.addWidget(title_label)

        profile_group = QGroupBox("--- Profile Setup ---")
        main_layout.addWidget(profile_group)

        profile_layout = QFormLayout()
        profile_group.setLayout(profile_layout)

        self.name_input = QLineEdit() # widget 1
        profile_layout.addRow("Enter Username:", self.name_input)
        self.allergies_input = QLineEdit() # widget 2
        self.allergies_input.setPlaceholderText("e.g., peanut, milk, soy, meat, gluten")
        profile_layout.addRow("Mention Allergies:", self.allergies_input)
        self.severity_dropdown = QComboBox() # widget 3
        self.severity_dropdown.addItems(["Severe (High Risk)", "Mild / Moderate (Low Risk)"])
        profile_layout.addRow("Mention Severity:", self.severity_dropdown)

        self.btn_register = QPushButton("Save & Lock Profile")
        profile_layout.addRow("", self.btn_register)

        check_group = QGroupBox("--- Live Meal Ingredient Scan ---")
        main_layout.addWidget(check_group)

        check_layout = QFormLayout()
        check_group.setLayout(check_layout)
        self.meal_input = QLineEdit() # widget 4
        check_layout.addRow("Enter Meal Title:", self.meal_input)
        self.ingredients_input = QTextEdit() # widget 5
        check_layout.addRow("Enter Ingredients:", self.ingredients_input)

        footer_layout = QHBoxLayout()
        main_layout.addLayout(footer_layout)

        self.btn_clear = QPushButton("Reset Form")
        self.btn_check = QPushButton("Run Safety Check")
        self.btn_exit = QPushButton("Exit App")

        footer_layout.addWidget(self.btn_clear)
        footer_layout.addWidget(self.btn_check)
        footer_layout.addWidget(self.btn_exit)

        self.btn_register.clicked.connect(self.handle_profile_registration) # signals and slots
        self.btn_check.clicked.connect(self.handle_meal_check)
        self.btn_clear.clicked.connect(self.handle_reset_form)
        self.btn_exit.clicked.connect(self.close)
        self.severity_dropdown.currentIndexChanged.connect(self.log_change)

    def log_change(self, index):
        print(f"[[System Log]]: Severity dropdown adjusted to selection index: {index}")

    def handle_profile_registration(self): #validation
        try:
            name = self.name_input.text().strip()
            raw_allergies = self.allergies_input.text().strip()
            if not name:
                raise SafeBiteValidationError("User Name cannot be left blank.")
            if not re.fullmatch(r"^[a-zA-Z\s]{2,20}$", name):
                raise SafeBiteValidationError("User Name must contain only alphabets (2-20 characters).")
            if not raw_allergies:
                raise SafeBiteValidationError("Please enter at least one allergy.")
            self.user_allergies = [a.strip().lower() for a in re.split(r"[,;]\s*", raw_allergies) if a.strip()]
            self.user_name = name
            self.severity_level = "Severe" if self.severity_dropdown.currentIndex() == 0 else "Mild"
            self.profile_registered = True
            QMessageBox.information(
                self,
                "Profile is Saved",
                f"Profile saved for {self.user_name}\nChecking and monitoring: {', '.join(self.user_allergies)}"
            )

        except SafeBiteValidationError as ve:
            QMessageBox.warning(self, "Validation warning", str(ve))

    def handle_meal_check(self):
        try:
            if not self.profile_registered:
                raise SafeBiteValidationError("Please save your profile details first")
            meal_title = self.meal_input.text().strip()
            ingredients_txt = self.ingredients_input.toPlainText().strip()
            if not meal_title or not ingredients_txt:
                raise SafeBiteValidationError("Both the meal title and ingredient blocks are required")

            dangerous_matches = [a for a in self.user_allergies if re.search(r"\b" + re.escape(a) + r"\b", ingredients_txt, re.IGNORECASE)]
            if dangerous_matches:
                if self.severity_level == "Severe":
                    QMessageBox.critical(
                        self, "DANGER", 
                        f"Unsafe ingredients found in {meal_title}\n\n"
                        f"Detected allergy causers: {', '.join(dangerous_matches).upper()}\nRisk level: high danger"
                    )
                else:
                    QMessageBox.warning(
                        self, "Warning", 
                        f"Note: {meal_title} contains {', '.join(dangerous_matches)}.\n\nRisk level: minor reaction/discomfort"
                    )
            else:
                QMessageBox.information(
                    self,
                    "Safe to Eat",
                    f"Clear and good, no allergy causers found in {meal_title}"
                )

        except SafeBiteValidationError as ve:
            QMessageBox.warning(self, "Checking incomplete", str(ve))

    def handle_reset_form(self):
        confirm = QMessageBox.question(
            self, "Confirm Reset", "Do you want to clear all form inputs and settings?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.name_input.clear()
            self.allergies_input.clear()
            self.meal_input.clear()
            self.ingredients_input.clear()
            self.severity_dropdown.setCurrentIndex(0)
            self.profile_registered = False

    def resizeEvent(self, event):
        new_size = event.size()
        print(f"[[Event Triggered]]: Window resized to {new_size.width()}x{new_size.height()}")
        super().resizeEvent(event)

    def mouseMoveEvent(self, event):
        x = event.position().x()
        y = event.position().y()
        print(f"[[Event Triggered]]: Mouse tracking coordinates -> X: {x:.0f}, Y: {y:.0f}")     
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            print("[[Event Triggered]]: Escape key clicked")
            self.close()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(
            self, "Confirm Exit", "Are you sure that you want to close SafeBite?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SafeBiteApp()
    window.show()
    sys.exit(app.exec())