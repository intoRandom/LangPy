<!--
Python español, Python français, Python português, learn Python native language,
Python transpiler, Python localization, Python i18n, Python education, beginner Python
-->

# LangPy

**Learn and write Python code in Spanish, French, Portuguese (more coming soon)** 🌍

LangPy is a lexical transpiler that lets you learn and write Python code using natural language keywords in Spanish (español), French (français), Portuguese (português), soon more - perfect for beginners and non-English speakers. Write `si` instead of `if`, `para` instead of `for`, with zero runtime overhead.

```python
# ejemplo.pyes (Spanish)
definir saludar(nombre):
    si nombre == "Ana":
        imprimir("Hola Ana")
    sino:
        imprimir("Hola", nombre)

saludar("Luis")
```

```bash
$ langpy ejemplo.pyes
Hola Luis
```

## Why LangPy?

LangPy makes Python more accessible to non-English speakers and complete beginners by allowing you to use natural language keywords. It's designed to help you focus on learning programming logic in your native language, while making it trivial to migrate to vanilla Python later - no additional tools or new concepts required, just rename your keywords when you're ready.

### What LangPy IS ✅

- A **lexical transpiler** that translates keywords to Python
- **100% compatible** with Python libraries and tools
- **Zero runtime overhead** - executes as native Python
- **Easy migration** path back to pure Python

### What LangPy is NOT ❌

- NOT a new programming language
- NOT a custom interpreter or VM
- NOT translating error messages or APIs
- NOT changing Python's semantics

**If something crosses these boundaries, it's out of scope.**

## Quick Start

### Installation

Requirements: Python 3.10+

```bash
pip install langpy
```

📚 **[Official Documentation](https://langpy.org)** - Complete guides, tutorials, and API reference

### Your First Program

Create a file `hello.pyes`:

```python
definir main():
    nombre = "World"
    imprimir(f"Hello {nombre}!")

main()
```

Run it:

```bash
langpy hello.pyes
```

That's it! LangPy transpiles your code to standard Python and executes it immediately.

## Supported Languages

| Language   | Extension | Keywords Example                  |
| ---------- | --------- | --------------------------------- |
| Spanish    | `.pyes`   | `para`, `si`, `sino`, `imprimir`  |
| French     | `.pyfr`   | `pour`, `si`, `sinon`, `imprimer` |
| Portuguese | `.pypt`   | `para`, `se`, `senao`, `imprimir` |

The language is determined **solely by the file extension**. No flags or configuration needed.

## Real-World Example

LangPy works seamlessly with local imports and external libraries.

**operations.pyes**

```python
definir suma(a, b):
    retornar a + b

definir resta(a, b):
    retornar a - b
```

**main.pyes**

```python
desde operations importar suma, resta
importar numpy como np

definir analizar_datos():
    # Use your functions
    resultado = suma(10, 5)
    imprimir(f"Suma: {resultado}")

    # Use any Python library
    datos = np.array([1, 2, 3, 4, 5])
    imprimir(f"Media: {np.mean(datos)}")

analizar_datos()
```

Run it:

```bash
langpy main.pyes
```

## Project Structure Support

LangPy supports Python-style package structures with `__main__` entry points:

```
mi_proyecto/
├── __main__.pyes          # Entry point
├── operations.pyes        # Local module
└── utils/
    ├── __init__.pyes
    └── helpers.pyes
```

Execute the entire project:

```bash
langpy mi_proyecto/
```

## Use Cases

- 🎓 **Learning Python** - Focus on programming logic in your native language
- 🌍 **Teaching** - Teach Python to non-English speaking students
- 🔄 **Gradual Migration** - Start in your language, migrate to English Python later
- 🛠️ **Prototyping** - Quick scripts without mental translation overhead
- 📚 **Educational Content** - Create programming tutorials in local languages

## How It Works

```
.pyes / .pypt / .pyfr file
        ↓
tokenize (Python stdlib)
        ↓
keyword replacement
        ↓
untokenize
        ↓
execute with Python VM
```

### Key Design Principles

- Only `NAME` tokens are translated (keywords)
- Strings and comments remain unchanged
- Attribute names are preserved (`obj.method`)
- No custom AST or parser
- If Python can't tokenize it, neither can LangPy

## CLI Usage

### Execute directly

```bash
# Run a file
langpy script.pyes

# Run a project directory (requires __main__.pyes)
langpy my_project/
```

### Transpile to Python

```bash
# Transpile in place (generates .py next to .pyes, resolves LangPy imports)
langpy transpile script.pyes

# Transpile to specific directory (resolves LangPy imports + copies vanilla .py files)
langpy transpile main.pyes --output dist/
langpy transpile main.pyes -o dist/  # short form
```

The `transpile` command:

- Always resolves and transpiles all local LangPy imports
- With `--output`: additionally copies referenced vanilla `.py` files (excludes pip modules)
- Preserves directory structure in output

### Extract (single-file mode)

For tooling integration (IDE extensions, linters):

```bash
# Extract to specific file
langpy extract input.pyes --output build/output.py

# Extract to directory (uses input filename)
langpy extract input.pyes --output build/
langpy extract input.pyes -o build/  # short form
```

The `extract` command transpiles a single file **without** resolving imports - useful for development tools.

### Force overwrite

```bash
langpy transpile script.pyes --force
langpy transpile script.pyes -f  # short form
```

### Get help

```bash
langpy --help
langpy --version
```

## Project Status

**Version:** 0.2.0

- ✅ Stable transpilation core
- ✅ Language lexicons defined
- ✅ Project structure support (`__main__` entry points)
- ✅ Import resolution and tree transpilation
- ✅ Output directory support with structure preservation
- ✅ Comprehensive test suite
- ✅ Clear project scope

## Contributing

LangPy's lexicon system is modular, making it easy to add new languages without modifying the core. Want to add your language? We'd love to have you contribute!

## License

MIT

---

**Made with ❤️ for the global Python community**
