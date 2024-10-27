import re

class Lexer:
    def __init__(self, content):
        self.content = content.splitlines()
        self.tokens = {}
        self.errors = []

        self.palabras_reservadas = [
            'si', 'mientras', 'hacer', 'entonces', 'entero', 'decimal', 'booleano',
            'cadena', 'sino', 'verdadero', 'falso'
        ]

        self.operadores = ['+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=']
        self.simbolos = ['(', ')', '{', '}', '"', ';', ',']  # Añadimos la coma a los símbolos

    def is_identificador(self, palabra):
        # Un identificador comienza con letra o guion bajo y sigue con letras o dígitos
        if palabra[0].isalpha() or palabra[0] == '_':
            return all(c.isalnum() or c == '_' for c in palabra)
        return False

    def is_numero(self, palabra):
        # Expresión regular para detectar enteros o decimales
        return bool(re.match(r'^\d+(\.\d+)?$', palabra))

    def is_operador(self, palabra):
        return palabra in self.operadores

    def is_simbolo(self, palabra):
        return palabra in self.simbolos

    def is_palabra_reservada(self, palabra):
        return palabra in self.palabras_reservadas

    def analyze(self):
        linea_actual = 0

        for linea in self.content:
            linea_actual += 1
            palabras = self.tokenize(linea)

            for palabra in palabras:
                if self.is_palabra_reservada(palabra):
                    self.agregar_token(palabra, 'PALABRA RESERVADA')
                elif self.is_identificador(palabra):
                    self.agregar_token(palabra, 'IDENTIFICADOR')
                elif self.is_numero(palabra):
                    self.agregar_token(palabra, 'NUMERO')
                elif self.is_operador(palabra):
                    self.agregar_token(palabra, 'OPERADOR')
                elif self.is_simbolo(palabra):
                    self.agregar_token(palabra, 'SIGNO')
                else:
                    self.errors.append({
                        'linea': linea_actual,
                        'mensaje': f"Token no reconocido: {palabra}"
                    })

        return self.tokens, self.errors

    def tokenize(self, linea):
        tokens = []
        token_actual = ''
        i = 0

        while i < len(linea):
            char = linea[i]

            if char in ('=', '!', '<', '>'):
                if i + 1 < len(linea) and linea[i + 1] == '=':
                    tokens.append(char + '=')
                    i += 1
                else:
                    tokens.append(char)
            elif char in self.operadores or char in self.simbolos:
                if token_actual:
                    tokens.append(token_actual)
                    token_actual = ''
                tokens.append(char)
            elif char.isspace():
                if token_actual:
                    tokens.append(token_actual)
                    token_actual = ''
            else:
                token_actual += char

            i += 1

        if token_actual:
            tokens.append(token_actual)

        return tokens

    def agregar_token(self, token, tipo):
        if token not in self.tokens:
            self.tokens[token] = {'tipo': tipo, 'cantidad': 1}
        else:
            self.tokens[token]['cantidad'] += 1
