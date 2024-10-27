import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit, QFileDialog, QLabel
from lexer import Lexer
from automata import Automata
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from FileManager import FileManager

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowIcon(QIcon("matrix.ico"))
        self.setWindowTitle("Analizador Léxico y Sintáctico")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #8193f5")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        H_layout = QHBoxLayout()
        label_layout = QHBoxLayout()

        self.intro_text = QLabel("Texto a analizar")
        self.intro_text.setAlignment(Qt.AlignCenter)
        label_layout.addWidget(self.intro_text)

        self.outro_text = QLabel("Tabla de operadores y análisis")
        self.outro_text.setAlignment(Qt.AlignCenter)
        label_layout.addWidget(self.outro_text)

        self.text_area = QTextEdit(self)
        self.text_area.setStyleSheet("background-color: #a3e2d2")
        H_layout.addWidget(self.text_area)

        self.load_button = QPushButton("Cargar Archivo")
        self.load_button.setStyleSheet("background-color: #ad81f5")
        self.load_button.clicked.connect(self.load_file)
        main_layout.addWidget(self.load_button)

        self.analyze_button = QPushButton("Analizar")
        self.analyze_button.setStyleSheet("background-color: #ad81f5")
        self.analyze_button.clicked.connect(self.analyze_file)
        main_layout.addWidget(self.analyze_button)

        self.close_button = QPushButton("Cerrar")
        self.close_button.setStyleSheet("background-color: #ad81f5")
        self.close_button.clicked.connect(self.close)
        main_layout.addWidget(self.close_button)

        self.result_area = QTextEdit(self)
        self.result_area.setStyleSheet("background-color: #a3e2d2")
        self.result_area.setReadOnly(True)

        H_layout.addWidget(self.result_area)

        main_layout.addLayout(label_layout)
        main_layout.addLayout(H_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
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

        automata = Automata(r"\bfuncion\b.*?\(.*?\)")
        descripcion_automata = automata.generar_descripcion()

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

            for token, data in tokens.items():
                result_msg += f"""
                <tr>
                    <td>{token}</td>
                    <td>{data['tipo']}</td>
                    <td>{data['cantidad']}</td>
                </tr>
                """

            result_msg += "</table>"
            result_msg += f"<br>{descripcion_automata}"
            self.result_area.setHtml(result_msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec_())
