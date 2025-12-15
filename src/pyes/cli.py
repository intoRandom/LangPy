# pyes/cli.py

import sys
from pathlib import Path

from pyes.core.transpiler import transpile
from pyes.core.lexicon.es import SpanishLexicon
from pyes.core.lexicon.pt import PortugueseLexicon
from pyes.core.lexicon.fr import FrenchLexicon


EXTENSION_TO_LEXICON = {
    ".pyes": SpanishLexicon,
    ".pypt": PortugueseLexicon,
    ".pyfr": FrenchLexicon,
}


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: pyes archivo")
        sys.exit(1)

    path = Path(sys.argv[1])

    if not path.exists() or not path.is_file():
        print(f"Archivo no encontrado: {path}")
        sys.exit(1)

    # Python-like behavior: script dir first in sys.path
    script_dir = str(path.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    source = path.read_text(encoding="utf-8")

    if path.suffix in EXTENSION_TO_LEXICON:
        lexicon = EXTENSION_TO_LEXICON[path.suffix]()
        source = transpile(source, lexicon)

    globals_context = {
        "__name__": "__main__",
        "__file__": str(path.resolve()),
        "__builtins__": __builtins__,
    }

    exec(compile(source, str(path), "exec"), globals_context)
