import argparse
from pathlib import Path

from generator import generate_python
from parser import ParserError, parse_code
from scanner import ScannerError, scanner
from semantic import SemanticError, validate_program


# -----------------------
# Programa principal
# -----------------------
# Une las etapas del traductor:
# 1. Scanner
# 2. Parser
# 3. Acciones semanticas
# 4. Generacion de codigo Python

def translate_file(input_path, output_path):
    source = input_path.read_text(encoding="utf-8")

    program = parse_code(source)
    validate_program(program)

    generated = generate_python(program)
    output_path.write_text(generated, encoding="utf-8")

    return generated


def print_tokens(source):
    for token in scanner(source):
        print(token)


def run_generated(code):
    namespace = {"__name__": "__main__"}
    exec(code, namespace)


def main():
    cli = argparse.ArgumentParser(
        description="Traductor del lenguaje de instalacion de paquetes."
    )
    cli.add_argument(
        "input",
        nargs="?",
        default="lenguaje.imb",
        help="Archivo fuente del lenguaje. Por defecto: lenguaje.imb",
    )
    cli.add_argument(
        "-o",
        "--output",
        help="Archivo Python de salida. Por defecto: mismo nombre con extension .py",
    )
    cli.add_argument(
        "--tokens",
        action="store_true",
        help="Muestra solo la salida del scanner.",
    )
    cli.add_argument(
        "--ast",
        action="store_true",
        help="Muestra el AST generado por el parser.",
    )
    cli.add_argument(
        "--run",
        action="store_true",
        help="Ejecuta el Python generado.",
    )

    args = cli.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".py")

    try:
        source = input_path.read_text(encoding="utf-8")

        if args.tokens:
            print_tokens(source)
            return

        program = parse_code(source)

        if args.ast:
            print(program)
            return

        validate_program(program)
        generated = generate_python(program)
        output_path.write_text(generated, encoding="utf-8")

    except ScannerError as exc:
        raise SystemExit(f"Error de scanner: {exc}") from exc
    except ParserError as exc:
        raise SystemExit(f"Error de parser: {exc}") from exc
    except SemanticError as exc:
        raise SystemExit(f"Error semantico: {exc}") from exc
    except FileNotFoundError as exc:
        raise SystemExit(f"No se encontro el archivo: {input_path}") from exc

    print(f"Traduccion generada en: {output_path}")

    if args.run:
        run_generated(generated)


if __name__ == "__main__":
    main()
