from generator import generate_python
from parser import parse_code
from semantic import validate_program


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

PAQUETE python2 {
    VERSION 2.7
}

PAQUETE libssl {
    VERSION 1.1
}

PAQUETE dev_tools {
    VERSION 1.0
}

SI entorno == "produccion" ENTONCES INSTALAR nodejs
SI entorno == "desarrollo" ENTONCES INSTALAR dev_tools
'''


programa = parse_code(data)
validate_program(programa)

codigo_python = generate_python(programa)

with open("leng_programas_automatizados.py", "w", encoding="utf-8") as archivo:
    archivo.write(codigo_python)

print("--- AST ---")
print(programa)

print("\n--- CODIGO GENERADO ---")
print(codigo_python)

print("\n--- EJECUCION ---")
exec(codigo_python)
