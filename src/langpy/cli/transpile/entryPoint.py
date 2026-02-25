import sys
from pathlib import Path


def _resolve_entry_point(path: Path) -> Path:
    """
    Si path es directorio, busca __main__.{ext}.
    Si es archivo, lo retorna tal cual.
    Lanza error si no encuentra nada válido.
    """
    if path.is_dir():
        for ext in [".pyes", ".pypt", ".pyfr"]:
            main_file = path / f"__main__{ext}"
            if main_file.exists():
                return main_file

        print(
            f"Error: directory must contain __main__.pyes, __main__.pypt, or __main__.pyfr")
        sys.exit(1)

    if not path.exists() or not path.is_file():
        print(f"Error: file not found: {path}")
        sys.exit(1)

    return path
