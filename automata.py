import re

class Automata:
    def __init__(self, expresion_regular):
        self.expresion_regular = expresion_regular
        self.patron = re.compile(expresion_regular)

    def evaluar_cadena(self, cadena):
        return bool(self.patron.fullmatch(cadena))

    def generar_descripcion(self):
        return f"Autómata generado para la expresión regular: {self.expresion_regular}"
