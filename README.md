# PyEs

PyEs es una capa léxica sobre Python que permite escribir código usando
palabras reservadas en español, sin cambiar el comportamiento de Python.

No es un lenguaje nuevo.
No tiene intérprete propio.
No modifica la semántica del código.
No traduce APIs ni librerías.

PyEs traduce **cómo se escribe el código**, no **lo que el código hace**.

---

## Qué es PyEs

- Un transpiler léxico
- Basado en `tokenize` de Python
- Traduce palabras reservadas en español a Python estándar
- Ejecuta el resultado con la VM de Python

El código PyEs:

- Se transpila a Python válido
- Se ejecuta con `exec`
- Puede usar cualquier librería Python
- Es fácilmente migrable a Python puro

---

## Qué NO es PyEs

PyEs **no**:

- Traduce mensajes de error
- Traduce APIs ni nombres de librerías
- Tiene parser propio
- Tiene AST propio
- Tiene runtime o VM propia
- Cambia el comportamiento de Python
- Es un lenguaje alternativo

Si una idea cruza alguno de estos puntos, está fuera del proyecto.

---

## Instalación

```bash
pip install pyes
```
