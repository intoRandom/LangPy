# pyes/__main__.py

import sys

from pyes.core.importer import PyEsFinder


def _register_import_hook():
    # Evitar registrar el finder más de una vez
    for finder in sys.meta_path:
        if isinstance(finder, PyEsFinder):
            return

    sys.meta_path.insert(0, PyEsFinder())


def main():
    _register_import_hook()

    # Import tardío a propósito: el hook debe existir antes
    from pyes.cli import main as cli_main

    cli_main()


if __name__ == "__main__":
    main()
