class Lexer:
    def __init__(self, content):
        self.content = content.splitlines()  # Divide el contenido en líneas
        self.tokens = {}
        self.errors = []

        # Lista de palabras reservadas
        self.palabras_reservadas = ['si', 'mientras', 'hacer', 'entonces']

        # Lista de operadores
        self.operadores = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=']

        # Lista de símbolos adicionales (como paréntesis)
        self.simbolos = ['(', ')']

    def is_identificador(self, palabra):
        # Identificador empieza con letra o guion bajo, seguido de letras, números o guion bajo
        if palabra[0].isalpha() or palabra[0] == '_':
            return all(c.isalnum() or c == '_' for c in palabra)
        return False

    def is_numero(self, palabra):
        return palabra.isdigit()

    def is_operador(self, palabra):
        return palabra in self.operadores

    def is_simbolo(self, palabra):
        return palabra in self.simbolos

    def is_palabra_reservada(self, palabra):
        return palabra in self.palabras_reservadas

    def analyze(self):
        linea_actual = 0

        # Analizar línea por línea
        for linea in self.content:
            linea_actual += 1
            palabras = self.tokenize(linea)  # Tokeniza la línea en palabras y símbolos

            for palabra in palabras:
                if self.is_palabra_reservada(palabra):
                    self.agregar_token(palabra, 'RESERVADA')
                elif self.is_identificador(palabra):
                    self.agregar_token(palabra, 'IDENTIFICADOR')
                elif self.is_numero(palabra):
                    self.agregar_token(palabra, 'NUMERO')
                elif self.is_operador(palabra):
                    self.agregar_token(palabra, 'OPERADOR')
                elif self.is_simbolo(palabra):
                    self.agregar_token(palabra, 'SIMBOLO')
                else:
                    self.errors.append({
                        'linea': linea_actual,
                        'mensaje': f"Token no reconocido: {palabra}"
                    })

        return self.tokens, self.errors

    def tokenize(self, linea):
        # Tokenización manual que separa operadores y símbolos de otros tokens
        tokens = []
        token_actual = ''
        i = 0

        while i < len(linea):
            char = linea[i]

            # Verificar operadores de dos caracteres
            if char in ('=', '!', '<', '>'):
                if i + 1 < len(linea) and linea[i + 1] == '=':
                    tokens.append(char + '=')  # Agregar operadores como '==', '!='
                    i += 1  # Saltar el siguiente carácter
                else:
                    tokens.append(char)  # Agregar solo el carácter actual
            elif char in self.operadores or char in self.simbolos:
                if token_actual:
                    tokens.append(token_actual)  # Agregar el token actual si existe
                    token_actual = ''
                tokens.append(char)  # Agregar el operador o símbolo
            elif char.isspace():
                if token_actual:
                    tokens.append(token_actual)  # Agregar el token actual si existe
                    token_actual = ''
            else:
                token_actual += char

            i += 1

        if token_actual:
            tokens.append(token_actual)  # Agregar el último token si existe

        return tokens

    def agregar_token(self, token, tipo):
        # Agregar el token al diccionario, o incrementar su cantidad
        if token not in self.tokens:
            self.tokens[token] = {'tipo': tipo, 'cantidad': 1}
        else:
            self.tokens[token]['cantidad'] += 1
