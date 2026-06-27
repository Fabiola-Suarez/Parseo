from dataclasses import dataclass, field

import ply.yacc as yacc

from scanner import lexer, tokens


# -----------------------
# Nodos del AST
# -----------------------

@dataclass
class Package:
    name: str
    version: str | None = None
    dependencies: list[str] = field(default_factory=list)
    optional: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)


@dataclass
class Condition:
    variable: str
    operator: str
    value: object
    package: str


@dataclass
class Program:
    variables: dict[str, object] = field(default_factory=dict)
    packages: dict[str, Package] = field(default_factory=dict)
    conditions: list[Condition] = field(default_factory=list)


class ParserError(Exception):
    pass


ast = Program()


# -----------------------
# GRAMATICA PRINCIPAL
# -----------------------

def p_programa(p):
    '''programa : sentencias'''
    program = Program()

    for sentencia in p[1]:
        tipo = sentencia[0]

        if tipo == "var":
            program.variables[sentencia[1]] = sentencia[2]

        elif tipo == "paquete":
            package = sentencia[1]

            if package.name in program.packages:
                raise ParserError(f"Paquete duplicado: {package.name}")

            program.packages[package.name] = package

        elif tipo == "si":
            program.conditions.append(sentencia[1])

    p[0] = program

    global ast
    ast = p[0]


# -----------------------
# SENTENCIAS
# -----------------------

def p_sentencias(p):
    '''sentencias : sentencia sentencias
                  | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_sentencia(p):
    '''sentencia : asignacion
                 | paquete
                 | condicional'''
    p[0] = p[1]


# -----------------------
# VARIABLES
# -----------------------

def p_asignacion(p):
    '''asignacion : VAR ID EQUALS valor'''
    p[0] = ("var", p[2], p[4])


def p_valor(p):
    '''valor : STRING
             | NUMBER
             | ID'''
    if isinstance(p[1], str) and p.slice[1].type == "NUMBER":
        if "." in p[1]:
            p[0] = float(p[1])
        else:
            p[0] = int(p[1])
    else:
        p[0] = p[1]


# -----------------------
# PAQUETES
# -----------------------

def p_paquete(p):
    '''paquete : PAQUETE ID LBRACE cuerpo_paquete RBRACE'''
    data = p[4]
    package = Package(
        name=p[2],
        version=data["version"],
        dependencies=data["dependencies"],
        optional=data["optional"],
        conflicts=data["conflicts"],
    )
    p[0] = ("paquete", package)


def p_cuerpo_paquete(p):
    '''cuerpo_paquete : sentencia_paquete cuerpo_paquete
                      | empty'''
    if len(p) == 3:
        data = empty_package_data()
        item_type, item_value = p[1]
        add_package_item(data, item_type, item_value)

        data["dependencies"] += p[2]["dependencies"]
        data["optional"] += p[2]["optional"]
        data["conflicts"] += p[2]["conflicts"]

        if p[2]["version"] is not None:
            data["version"] = p[2]["version"]

        p[0] = data
    else:
        p[0] = empty_package_data()


def p_sentencia_paquete(p):
    '''sentencia_paquete : VERSION NUMBER
                         | DEPENDE ID
                         | REQUIERE ID
                         | OPCIONAL ID
                         | CONFLICTO ID'''
    if p.slice[1].type == "VERSION":
        p[0] = ("version", p[2])
    elif p.slice[1].type in ("DEPENDE", "REQUIERE"):
        p[0] = ("dependencies", p[2])
    elif p.slice[1].type == "OPCIONAL":
        p[0] = ("optional", p[2])
    else:
        p[0] = ("conflicts", p[2])


def empty_package_data():
    return {
        "version": None,
        "dependencies": [],
        "optional": [],
        "conflicts": [],
    }


def add_package_item(data, item_type, item_value):
    if item_type == "version":
        data["version"] = item_value
    else:
        data[item_type].append(item_value)


# -----------------------
# CONDICIONALES
# -----------------------

def p_condicional(p):
    '''condicional : SI ID operador valor ENTONCES INSTALAR ID'''
    condition = Condition(
        variable=p[2],
        operator=p[3],
        value=p[4],
        package=p[7],
    )
    p[0] = ("si", condition)


def p_operador(p):
    '''operador : EQ
                | GT'''
    p[0] = p[1]


# -----------------------
# VACIO / ERROR
# -----------------------

def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
        raise ParserError(f"Error de sintaxis en '{p.value}'")
    raise ParserError("Error de sintaxis: fin inesperado")


parser = yacc.yacc(write_tables=False, debug=False)


def parse_code(data):
    global ast
    ast = Program()
    lexer.lineno = 1
    result = parser.parse(data, lexer=lexer)
    return result


# -----------------------
# Prueba
# -----------------------

if __name__ == "__main__":
    data = '''
VAR entorno = "desarrollo"

PAQUETE nodejs {
    VERSION 18.0
    DEPENDE libssl
}

PAQUETE libssl {
    VERSION 1.1
}

SI entorno == "desarrollo" ENTONCES INSTALAR nodejs
'''

    ast = parse_code(data)
    print(ast)
