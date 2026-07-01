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

if entorno == 'produccion':
    if 'libssl' not in instalados:
        print('Instalando: libssl')
        instalados.append('libssl')

    if 'python2' in instalados:
        raise RuntimeError('Incompatibilidad: python entra en conflicto con python2')

    if 'python' not in instalados:
        print('Instalando: python')
        instalados.append('python')

    if 'nodejs' not in instalados:
        print('Instalando: nodejs')
        instalados.append('nodejs')

if entorno == 'desarrollo':
    if 'dev_tools' not in instalados:
        print('Instalando: dev_tools')
        instalados.append('dev_tools')

print('Orden de instalacion:', ' -> '.join(instalados) if instalados else '(sin instalaciones)')
