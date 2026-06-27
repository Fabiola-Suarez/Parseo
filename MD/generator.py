from pprint import pformat


# -----------------------
# Generador de codigo
# -----------------------

def package_to_dict(package):
    return {
        "version": package.version,
        "dependencias": package.dependencies,
        "opcionales": package.optional,
        "conflictos": package.conflicts,
    }


def dependency_order(package_name, packages):
    order = []
    visited = set()
    stack = [(package_name, False)]

    while stack:
        current, expanded = stack.pop()

        if expanded:
            if current not in visited:
                visited.add(current)
                order.append(current)
            continue

        if current in visited:
            continue

        stack.append((current, True))

        dependencies = packages[current].dependencies
        index = len(dependencies) - 1
        while index >= 0:
            dependency = dependencies[index]
            if dependency not in visited:
                stack.append((dependency, False))
            index -= 1

    return order


def emit_conflict_checks(output, package_name, packages, indent):
    package = packages[package_name]

    for conflict in package.conflicts:
        output.extend(
            [
                f"{indent}if {conflict!r} in instalados:",
                f"{indent}    raise RuntimeError('Incompatibilidad: {package_name} entra en conflicto con {conflict}')",
                "",
            ]
        )

    for installed_name, installed_package in packages.items():
        if package_name in installed_package.conflicts:
            output.extend(
                [
                    f"{indent}if {installed_name!r} in instalados:",
                    f"{indent}    raise RuntimeError('Incompatibilidad: {package_name} entra en conflicto con {installed_name}')",
                    "",
                ]
            )


def emit_install_package(output, package_name, packages, indent):
    emit_conflict_checks(output, package_name, packages, indent)
    output.extend(
        [
            f"{indent}if {package_name!r} not in instalados:",
            f"{indent}    print('Instalando: {package_name}')",
            f"{indent}    instalados.append({package_name!r})",
            "",
        ]
    )


def generate_python(program):
    packages = {
        name: package_to_dict(package)
        for name, package in sorted(program.packages.items())
    }

    output = [
        "# Archivo generado automaticamente desde el lenguaje .imb",
        "# No usa recursividad: el traductor deja el orden de instalacion resuelto.",
        "",
    ]

    for name, value in program.variables.items():
        output.append(f"{name} = {value!r}")

    output.extend(
        [
            "",
            f"paquetes = {pformat(packages, sort_dicts=False)}",
            "",
            "instalados = []",
            "",
        ]
    )

    for condition in program.conditions:
        comparison = f"{condition.variable} {condition.operator} {condition.value!r}"
        output.extend(
            [
                f"if {comparison}:",
            ]
        )

        for package_name in dependency_order(condition.package, program.packages):
            emit_install_package(output, package_name, program.packages, "    ")

    output.extend(
        [
            "print('Orden de instalacion:', ' -> '.join(instalados) if instalados else '(sin instalaciones)')",
            "",
        ]
    )

    return "\n".join(output)
