import ast
import re
from dataclasses import dataclass


# -----------------------
# Palabras reservadas
# -----------------------
# Son las palabras propias del lenguaje.
# No se toman como identificadores comunes.

reserved = {
    "VAR": "VAR",
    "PAQUETE": "PAQUETE",
    "VERSION": "VERSION",
    "DEPENDE": "DEPENDE",
    "REQUIERE": "REQUIERE",
    "OPCIONAL": "OPCIONAL",
    "CONFLICTO": "CONFLICTO",
    "SI": "SI",
    "ENTONCES": "ENTONCES",
    "INSTALAR": "INSTALAR",
}


# -----------------------
# Tokens
# -----------------------
# Estos son los elementos minimos que reconoce el scanner.

tokens = [
    "ID",
    "STRING",
    "NUMBER",

    # Operadores
    "EQUALS",
    "EQ",
    "GT",

    # Simbolos
    "LBRACE",
    "RBRACE",
] + list(reserved.values())


# -----------------------
# Clase Token
# -----------------------
# Guarda tipo, valor y posicion para poder explicar errores.

@dataclass
class Token:
    type: str
    value: object
    line: int
    column: int
    lexeme: str


class ScannerError(Exception):
    pass


# -----------------------
# Expresiones regulares
# -----------------------
# El orden importa: primero se reconocen operadores largos como ==.

token_patterns = [
    ("EQ", r"=="),
    ("EQUALS", r"="),
    ("GT", r">"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("STRING", r'"([^\\\n]|(\\.))*?"'),
    ("NUMBER", r"\d+(\.\d+)?"),
    ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
]


# -----------------------
# Construccion del scanner
# -----------------------
# Recorre el codigo fuente y devuelve una lista de tokens.

def scanner(data):
    token_list = []

    for line_number, raw_line in enumerate(data.splitlines(), start=1):
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
            continue

        position = 0

        while position < len(line):
            character = line[position]

            if character.isspace():
                position += 1
                continue

            matched = False

            for token_type, pattern in token_patterns:
                match = re.match(pattern, line[position:])

                if match:
                    lexeme = match.group(0)
                    value = lexeme

                    if token_type == "STRING":
                        value = ast.literal_eval(lexeme)

                    elif token_type == "NUMBER":
                        value = lexeme

                    elif token_type == "ID":
                        token_type = reserved.get(lexeme, "ID")

                    token_list.append(
                        Token(
                            type=token_type,
                            value=value,
                            line=line_number,
                            column=position + 1,
                            lexeme=lexeme,
                        )
                    )

                    position += len(lexeme)
                    matched = True
                    break

            if not matched:
                raise ScannerError(
                    f"Caracter ilegal '{character}' en linea {line_number}, "
                    f"columna {position + 1}"
                )

    return token_list


# -----------------------
# Prueba
# -----------------------
# Este ejemplo permite mostrar el scanner funcionando.

if __name__ == "__main__":
    data = '''
VAR entorno = "desarrollo"
VAR paquete = nodejs
VAR version = 18.0

PAQUETE nodejs {
    VERSION 18.0
    DEPENDE libssl
    DEPENDE python
}

PAQUETE python {
    VERSION 3.10
    DEPENDE libssl
    CONFLICTO python2
}

SI entorno == "desarrollo" ENTONCES INSTALAR nodejs
'''

    for token in scanner(data):
        print(token)
