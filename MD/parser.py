from dataclasses import dataclass, field

from scanner import Token, scanner


# -----------------------
# Nodos del AST
# -----------------------
# Estas clases representan la estructura del programa ya parseado.

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


# -----------------------
# Parser
# -----------------------
# Consume los tokens del scanner y arma un AST.

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def current(self):
        return self.tokens[self.index]

    def check(self, token_type):
        return self.current().type == token_type

    def advance(self):
        token = self.current()
        if not self.check("EOF"):
            self.index += 1
        return token

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        token = self.current()
        raise ParserError(
            f"{message}. Recibido {token.type} ({token.lexeme!r}) "
            f"en linea {token.line}, columna {token.column}"
        )

    def parse(self):
        program = Program()

        while not self.check("EOF"):
            if self.check("VAR"):
                name, value = self.parse_assignment()
                program.variables[name] = value

            elif self.check("PAQUETE"):
                package = self.parse_package()

                if package.name in program.packages:
                    raise ParserError(f"Paquete duplicado: {package.name}")

                program.packages[package.name] = package

            elif self.check("SI"):
                program.conditions.append(self.parse_condition())

            else:
                token = self.current()
                raise ParserError(
                    f"Instruccion inesperada {token.lexeme!r} "
                    f"en linea {token.line}, columna {token.column}"
                )

        return program

    def parse_assignment(self):
        self.consume("VAR", "Se esperaba VAR")
        name = self.consume("ID", "Se esperaba el nombre de la variable").value
        self.consume("EQUALS", "Se esperaba '=' en la asignacion")
        value = self.parse_value()
        return name, value

    def parse_package(self):
        self.consume("PAQUETE", "Se esperaba PAQUETE")
        name = self.consume("ID", "Se esperaba el nombre del paquete").value
        self.consume("LBRACE", "Se esperaba '{' para abrir el paquete")

        package = Package(name=name)

        while not self.check("RBRACE"):
            if self.check("EOF"):
                raise ParserError(f"Falta cerrar el paquete {name} con '}}'")

            keyword = self.advance()

            if keyword.type == "VERSION":
                version = self.consume("NUMBER", f"La VERSION de {name} debe ser numerica")
                package.version = version.lexeme

            elif keyword.type in ("DEPENDE", "REQUIERE"):
                dependency = self.consume("ID", f"{keyword.type} espera un identificador")
                package.dependencies.append(dependency.value)

            elif keyword.type == "OPCIONAL":
                optional = self.consume("ID", "OPCIONAL espera un identificador")
                package.optional.append(optional.value)

            elif keyword.type == "CONFLICTO":
                conflict = self.consume("ID", "CONFLICTO espera un identificador")
                package.conflicts.append(conflict.value)

            else:
                raise ParserError(
                    f"Palabra reservada desconocida en {name}: {keyword.lexeme!r} "
                    f"linea {keyword.line}, columna {keyword.column}"
                )

        self.consume("RBRACE", "Se esperaba '}' para cerrar el paquete")
        return package

    def parse_condition(self):
        self.consume("SI", "Se esperaba SI")
        variable = self.consume("ID", "Se esperaba una variable en la condicion").value

        if self.check("EQ") or self.check("GT"):
            operator = self.advance().lexeme
        else:
            raise ParserError("Se esperaba un operador de comparacion: == o >")

        value = self.parse_value()
        self.consume("ENTONCES", "Se esperaba ENTONCES")
        self.consume("INSTALAR", "Se esperaba INSTALAR")
        package = self.consume("ID", "Se esperaba el paquete a instalar").value

        return Condition(variable=variable, operator=operator, value=value, package=package)

    def parse_value(self):
        if self.check("NUMBER"):
            token = self.advance()
            if "." in token.value:
                return float(token.value)
            return int(token.value)

        if self.check("STRING") or self.check("ID"):
            return self.advance().value

        token = self.current()
        raise ParserError(
            f"Se esperaba un valor, recibido {token.type} ({token.lexeme!r}) "
            f"en linea {token.line}, columna {token.column}"
        )


# -----------------------
# Funcion publica
# -----------------------
# Esta funcion conecta scanner + parser.

def parse_code(data):
    token_list = scanner(data)
    token_list.append(Token("EOF", None, 0, 0, ""))
    parser = Parser(token_list)
    return parser.parse()


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
