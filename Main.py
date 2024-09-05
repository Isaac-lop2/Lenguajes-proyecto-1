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
            error_msg = "<b>Errores léxicos encontrados:</b><br>"
            for error in errors:
                error_msg += f"Línea {error['linea']}: {error['mensaje']}<br>"
            self.result_area.setHtml(error_msg)
        else:
            result_msg = """
            <style>
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin-top: 20px;
            }
            th, td {
                padding: 8px 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
                font-family: Arial, sans-serif;
            }
            th {
                background-color: #f2f2f2;
            }
            </style>
            <table>
                <tr>
                    <th>TOKEN</th>
                    <th>TIPO</th>
                    <th>CANTIDAD</th>
                </tr>
            """

            # Añadir filas de tokens
            for token, data in tokens.items():
                result_msg += f"""
                <tr>
                    <td>{token}</td>
                    <td>{data['tipo']}</td>
                    <td>{data['cantidad']}</td>
                </tr>
                """

            result_msg += "</table>"
            self.result_area.setHtml(result_msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec_())
