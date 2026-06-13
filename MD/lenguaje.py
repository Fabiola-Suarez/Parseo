# Archivo generado automaticamente desde el lenguaje .imb

entorno = 'desarrollo'
paquete = 'nodejs'
version = 18.0

paquetes = {'dev_tools': {'version': '1.0',
               'dependencias': [],
               'opcionales': [],
               'conflictos': []},
 'libssl': {'version': '1.1',
            'dependencias': [],
            'opcionales': [],
            'conflictos': []},
 'nodejs': {'version': '18.0',
            'dependencias': ['libssl', 'python'],
            'opcionales': [],
            'conflictos': []},
 'python': {'version': '3.10',
            'dependencias': ['libssl'],
            'opcionales': [],
            'conflictos': ['python2']},
 'python2': {'version': '2.7',
             'dependencias': [],
             'opcionales': [],
             'conflictos': []}}

instalados = []


def validar_conflictos(nombre):
    paquete = paquetes[nombre]
    conflictos = set(paquete.get('conflictos', []))
    validar_conflictos_desde(nombre, conflictos, 0)


def validar_conflictos_desde(nombre, conflictos, indice):
    if indice < len(instalados):
        instalado = instalados[indice]
        conflictos_instalado = set(paquetes[instalado].get('conflictos', []))

        if instalado in conflictos or nombre in conflictos_instalado:
            raise RuntimeError(
                f'Incompatibilidad: {nombre} entra en conflicto con {instalado}'
            )

        validar_conflictos_desde(nombre, conflictos, indice + 1)


def instalar_dependencias(dependencias, indice):
    if indice < len(dependencias):
        instalar(dependencias[indice])
        instalar_dependencias(dependencias, indice + 1)


def instalar(nombre):
    if nombre in instalados:
        return

    if nombre not in paquetes:
        raise RuntimeError(f'Paquete desconocido: {nombre}')

    dependencias = paquetes[nombre].get('dependencias', [])
    instalar_dependencias(dependencias, 0)

    validar_conflictos(nombre)
    print(f'Instalando: {nombre}')
    instalados.append(nombre)

if entorno == 'produccion':
    instalar('nodejs')

if entorno == 'desarrollo':
    instalar('dev_tools')

print('Orden de instalacion:', ' -> '.join(instalados) if instalados else '(sin instalaciones)')
