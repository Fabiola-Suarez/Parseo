# Parseo y Generación de Código
- Repositorio de la materia "Parseo y Generación de Código" Dictada en la Universidad Nacional de Hurlingham,  durante el primer cuatrimestre del año 2026. <br>
- Profesor: Pablo Pandolfo <br>
- Alumna: Fabiola Suarez
---
### Trabajos Final
- [Traductor](https://github.com/Fabiola-Suarez/Parseo/blob/main/MD/app.ipynb)
- [Leng_programas_automatizados](https://github.com/Fabiola-Suarez/Parseo/blob/main/MD/leng_programas_automatizados.py)
- [Scanner](https://github.com/Fabiola-Suarez/Parseo/blob/main/MD/scanner.py)
- [Parser](https://github.com/Fabiola-Suarez/Parseo/blob/main/MD/parser.py)
- [Main](https://github.com/Fabiola-Suarez/Parseo/blob/main/MD/main.py)
- [Pruebas](https://github.com/Fabiola-Suarez/Parseo/blob/main/MD/tests.py)

---

### Conclusiones

En este trabajo diseñe la implementacion de un lenguaje orientado a la automatizacion de instalacion de programas en Linux. El lenguaje permite declarar variables, definir paquetes, indicar versiones, establecer dependencias, marcar conflictos y ejecutar instalaciones segun las condiciones.

En el desarrollo del scanner se obserba que el analisis lexico separa el codigo fuente en tokens reconocibles por el parser. Luego, el parser, define la estructura sintactica valida del lenguaje y se construye la representacion interna del programa.

Las acciones semanticas validan reglas que no dependen solamente de la sintaxis, como verificar que los paquetes tengan version, que las dependencias existan, que las variables usadas en condiciones hayan sido declaradas y que no se intente instalar un paquete que no existe.

Finalmente, el generador de codigo tradujo el lenguaje creado a Python. El codigo resuelve el orden de instalacion de dependencias y utiliza condicionales para decidir que paquetes instalar.

Como mejora futura, el lenguaje podria ampliarse con nuevas instrucciones, mas operadores de comparacion, soporte para distintas distribuciones de Linux o generacion de comandos reales de instalacion como `apt install` o `dnf install`.


