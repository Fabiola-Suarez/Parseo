class SemanticError(Exception):
    pass


# -----------------------
# Acciones semanticas
# -----------------------
# Validan reglas que no son solo sintaxis.

def validate_program(program):
    validate_packages(program)
    validate_conditions(program)


def validate_packages(program):
    for package in program.packages.values():
        if package.version is None:
            raise SemanticError(f"El paquete '{package.name}' no tiene VERSION")

        validate_references(
            package.name,
            "dependencia",
            package.dependencies,
            program.packages,
        )

        validate_references(
            package.name,
            "paquete opcional",
            package.optional,
            program.packages,
        )

        validate_references(
            package.name,
            "conflicto",
            package.conflicts,
            program.packages,
        )

        if package.name in package.conflicts:
            raise SemanticError(f"El paquete '{package.name}' no puede conflictuar consigo mismo")


def validate_references(package_name, reference_type, references, packages):
    for reference in references:
        if reference not in packages:
            raise SemanticError(
                f"El paquete '{package_name}' declara {reference_type} "
                f"'{reference}', pero ese paquete no existe"
            )


def validate_conditions(program):
    for condition in program.conditions:
        if condition.variable not in program.variables:
            raise SemanticError(
                f"La condicion usa la variable '{condition.variable}', "
                "pero no fue declarada con VAR"
            )

        if condition.package not in program.packages:
            raise SemanticError(
                f"La condicion intenta instalar '{condition.package}', "
                "pero ese paquete no fue declarado"
            )


# -----------------------
# Prueba
# -----------------------

if __name__ == "__main__":
    from parser import parse_code

    data = '''
VAR entorno = "desarrollo"

PAQUETE libssl {
    VERSION 1.1
}

SI entorno == "desarrollo" ENTONCES INSTALAR libssl
'''

    program = parse_code(data)
    validate_program(program)
    print("Validacion semantica correcta")
