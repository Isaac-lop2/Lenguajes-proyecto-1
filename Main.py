import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QFileDialog, QMessageBox
from lexer import Lexer
from FileManager import FileManager

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Analizador Léxico")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #E0EBFF")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.text_area = QTextEdit(self)
        layout.addWidget(self.text_area)

        self.load_button = QPushButton("Cargar Archivo")
        self.load_button.clicked.connect(self.load_file)
        layout.addWidget(self.load_button)

        self.analyze_button = QPushButton("Analizar")
        self.analyze_button.clicked.connect(self.analyze_file)
        layout.addWidget(self.analyze_button)

        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Abrir archivo de texto", "", "Text Files (*.txt)")
        if file_path:
            file_content = FileManager.read_file(file_path)
            self.text_area.setText(file_content)

    def analyze_file(self):
        file_content = self.text_area.toPlainText()
        lexer = Lexer(file_content)
        tokens, errors = lexer.analyze()

        if errors:
            pass
        else:
            result_msg = "TOKEN\tTIPO\tCANTIDAD\n"
            pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec_())
