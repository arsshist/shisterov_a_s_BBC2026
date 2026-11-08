import sys

from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ReadingPlanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Читай по плану")
        self.setMinimumWidth(380)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.addWidget(QLabel("Рассчитайте дневную норму чтения"))

        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("Например, 250")

        self.deadline = QComboBox()
        self.deadline.setEditable(True)
        self.deadline.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.deadline.addItems(["7", "14", "30"])

        form = QFormLayout()
        form.addRow("Осталось страниц", self.pages_input)
        form.addRow("Срок чтения (в днях)", self.deadline)
        layout.addLayout(form)

        calculate_button = QPushButton("Рассчитать")
        calculate_button.clicked.connect(self.calculate)
        self.pages_input.returnPressed.connect(self.calculate)
        self.deadline.lineEdit().returnPressed.connect(self.calculate)
        layout.addWidget(calculate_button)

        self.result = QLabel()
        self.result.setWordWrap(True)
        layout.addWidget(self.result)
        self.pages_input.setFocus()

    def calculate(self):
        pages = self.read_positive_int(self.pages_input, "Осталось страниц")
        if pages is None:
            return

        days = self.read_positive_int(self.deadline.lineEdit(), "Срок чтения (в днях)")
        if days is None:
            return

        # Округляем вверх, чтобы успеть дочитать книгу в срок.
        pages_per_day = (pages + days - 1) // days
        self.result.setText(f"Дневная норма: {pages_per_day} стр. в день.")

    def read_positive_int(self, field, label):
        try:
            number = int(field.text().strip())
            if number <= 0:
                raise ValueError
        except ValueError:
            self.result.clear()
            QMessageBox.warning(
                self, "Ошибка ввода", f"В поле «{label}» введите целое число больше нуля."
            )
            field.setFocus()
            field.selectAll()
            return None
        return number


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReadingPlanner()
    window.show()
    sys.exit(app.exec())
