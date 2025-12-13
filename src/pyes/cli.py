import sys
from pathlib import Path

from pyes.core.transpiler import transpile
from pyes.core.lexicon.es import SpanishLexicon


def get_lexicon(lang: str = "es"):
    if lang == "es":
        return SpanishLexicon()
    raise ValueError(f"Idioma no soportado: {lang}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: pyes archivo.pyes")
        sys.exit(1)

    path = Path(sys.argv[1])

    if not path.exists() or not path.is_file():
        print(f"Archivo no encontrado: {path}")
        sys.exit(1)

    if path.suffix != ".pyes":
        print("El archivo debe tener extensión .pyes")
        sys.exit(1)

    source = path.read_text(encoding="utf-8")

    lexicon = get_lexicon("es")
    output = transpile(source, lexicon)

    globals_context = {
        "__name__": "__main__",
        "__file__": str(path.resolve()),
        "__builtins__": __builtins__,
    }

    exec(output, globals_context)
