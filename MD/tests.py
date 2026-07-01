from generator import generate_python
from parser import ParserError, parse_code
from semantic import SemanticError, validate_program


def probar_valido(nombre, codigo):
    print(f"\n[OK esperado] {nombre}")

    programa = parse_code(codigo)
    validate_program(programa)
    codigo_python = generate_python(programa)

    print("Prueba superada")
    return codigo_python


def probar_error_semantico(nombre, codigo):
    print(f"\n[ERROR semantico esperado] {nombre}")

    try:
        programa = parse_code(codigo)
        validate_program(programa)
        print("FALLO: se esperaba un error semantico")
    except SemanticError as error:
        print(f"Prueba superada: {error}")


def probar_error_sintactico(nombre, codigo):
    print(f"\n[ERROR sintactico esperado] {nombre}")

    try:
        programa = parse_code(codigo)
        validate_program(programa)
        print("FALLO: se esperaba un error sintactico")
    except ParserError as error:
        print(f"Prueba superada: {error}")


def ejecutar_pruebas():
    probar_valido(
        "instalacion simple",
        '''
VAR entorno = "desarrollo"

PAQUETE dev_tools {
    VERSION 1.0
}

SI entorno == "desarrollo" ENTONCES INSTALAR dev_tools
''',
    )

    probar_valido(
        "instalacion con dependencia",
        '''
VAR entorno = "produccion"

PAQUETE nodejs {
    VERSION 18.0
    DEPENDE libssl
}

PAQUETE libssl {
    VERSION 1.1
}

SI entorno == "produccion" ENTONCES INSTALAR nodejs
''',
    )

    probar_error_semantico(
        "dependencia inexistente",
        '''
VAR entorno = "produccion"

PAQUETE nodejs {
    VERSION 18.0
    DEPENDE libssl
}

SI entorno == "produccion" ENTONCES INSTALAR nodejs
''',
    )

    probar_error_semantico(
        "variable no declarada",
        '''
PAQUETE dev_tools {
    VERSION 1.0
}

SI entorno == "desarrollo" ENTONCES INSTALAR dev_tools
''',
    )

    probar_error_semantico(
        "paquete sin version",
        '''
VAR entorno = "desarrollo"

PAQUETE dev_tools {
}

SI entorno == "desarrollo" ENTONCES INSTALAR dev_tools
''',
    )

    probar_error_semantico(
        "paquete a instalar no declarado",
        '''
VAR entorno = "desarrollo"

PAQUETE libssl {
    VERSION 1.1
}

SI entorno == "desarrollo" ENTONCES INSTALAR nodejs
''',
    )

    probar_error_sintactico(
        "falta operador de asignacion",
        '''
VAR entorno "desarrollo"

PAQUETE dev_tools {
    VERSION 1.0
}
''',
    )


if __name__ == "__main__":
    ejecutar_pruebas()
