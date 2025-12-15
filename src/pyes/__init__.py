# pyes/__init__.py

import sys
from pyes.core.importer import PyEsFinder


def _register_import_hook():
    for finder in sys.meta_path:
        if isinstance(finder, PyEsFinder):
            return
    sys.meta_path.insert(0, PyEsFinder())


_register_import_hook()
