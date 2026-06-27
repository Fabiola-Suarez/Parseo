import ast

import ply.lex as lex


# -----------------------
# Palabras reservadas
# -----------------------

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

tokens = (
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
) + tuple(reserved.values())


# -----------------------
# Patrones simples
# -----------------------

t_EQ = r"=="
t_EQUALS = r"="
t_GT = r">"
t_LBRACE = r"\{"
t_RBRACE = r"\}"


# -----------------------
# Tokens con acciones
# -----------------------

def t_STRING(t):
    r'"([^\\\n]|(\\.))*?"|\'([^\\\n]|(\\.))*?\''
    t.lexeme = t.value
    t.value = ast.literal_eval(t.value)
    return t


def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.lexeme = t.value
    return t


def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.lexeme = t.value
    t.type = reserved.get(t.value, "ID")
    return t


# -----------------------
# Ignorar espacios, tabs y comentarios
# -----------------------

t_ignore = " \t"


def t_COMMENT(t):
    r"\#.*"
    pass


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)


# -----------------------
# Construir scanner
# -----------------------

lexer = lex.lex()


# -----------------------
# Prueba
# -----------------------

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

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
