from pprint import pformat


# -----------------------
# Generador de codigo
# -----------------------
# Recibe el AST validado y genera codigo Python.

def package_to_dict(package):
    return {
        "version": package.version,
        "dependencias": package.dependencies,
        "opcionales": package.optional,
        "conflictos": package.conflicts,
    }


def generate_python(program):
    packages = {
        name: package_to_dict(package)
        for name, package in sorted(program.packages.items())
    }

    output = [
        "# Archivo generado automaticamente desde el lenguaje .imb",
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
            "",
            "def validar_conflictos(nombre):",
            "    paquete = paquetes[nombre]",
            "    conflictos = set(paquete.get('conflictos', []))",
            "    validar_conflictos_desde(nombre, conflictos, 0)",
            "",
            "",
            "def validar_conflictos_desde(nombre, conflictos, indice):",
            "    if indice < len(instalados):",
            "        instalado = instalados[indice]",
            "        conflictos_instalado = set(paquetes[instalado].get('conflictos', []))",
            "",
            "        if instalado in conflictos or nombre in conflictos_instalado:",
            "            raise RuntimeError(",
            "                f'Incompatibilidad: {nombre} entra en conflicto con {instalado}'",
            "            )",
            "",
            "        validar_conflictos_desde(nombre, conflictos, indice + 1)",
            "",
            "",
            "def instalar_dependencias(dependencias, indice):",
            "    if indice < len(dependencias):",
            "        instalar(dependencias[indice])",
            "        instalar_dependencias(dependencias, indice + 1)",
            "",
            "",
            "def instalar(nombre):",
            "    if nombre in instalados:",
            "        return",
            "",
            "    if nombre not in paquetes:",
            "        raise RuntimeError(f'Paquete desconocido: {nombre}')",
            "",
            "    dependencias = paquetes[nombre].get('dependencias', [])",
            "    instalar_dependencias(dependencias, 0)",
            "",
            "    validar_conflictos(nombre)",
            "    print(f'Instalando: {nombre}')",
            "    instalados.append(nombre)",
            "",
        ]
    )

    for condition in program.conditions:
        comparison = f"{condition.variable} {condition.operator} {condition.value!r}"
        output.extend(
            [
                f"if {comparison}:",
                f"    instalar({condition.package!r})",
                "",
            ]
        )

    output.extend(
        [
            "print('Orden de instalacion:', ' -> '.join(instalados) if instalados else '(sin instalaciones)')",
            "",
        ]
    )

    return "\n".join(output)
