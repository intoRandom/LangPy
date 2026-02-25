import sys
from pathlib import Path
from importlib.metadata import version
import argparse

from langpy.cli.messages import info, help
from langpy.cli.transpile.entryPoint import _resolve_entry_point
from langpy.cli.transpile.tree import transpile_tree
from langpy.cli.transpile.transpiler import (
    _transpile_file,
    _transpile_to_memory,
)


class CustomHelpAction(argparse.Action):
    """Custom action to show our help message instead of argparse's."""

    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(help())
        parser.exit()


def main() -> None:
    # Deshabilitar ayuda automática de argparse
    parser = argparse.ArgumentParser(
        prog="langpy",
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Flags globales
    parser.add_argument(
        "--help", "-h",
        action=CustomHelpAction,
        help="Show help message",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=version("langpy"),
    )

    # Subcomandos
    subparsers = parser.add_subparsers(dest="command")

    # ---- transpile ----
    transpile_parser = subparsers.add_parser(
        "transpile",
        help="Transpile file or directory resolving imports",
        add_help=False,
    )
    transpile_parser.add_argument("path", type=Path)
    transpile_parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    transpile_parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output directory for transpiled files",
    )
    transpile_parser.add_argument(
        "-h", "--help",
        action=CustomHelpAction,
        help="Show help message",
    )

    # ---- extract (hidden, for tooling/dev only) ----
    extract_parser = subparsers.add_parser(
        "extract",
        help="Transpile single file ignoring imports (dev/tooling only)",
        add_help=False,
    )
    extract_parser.add_argument("input", type=Path)
    extract_parser.add_argument(
        "-o", "--output",
        type=Path,
        required=True,
        help="Output file or directory",
    )
    extract_parser.add_argument(
        "-h", "--help",
        action=CustomHelpAction,
        help="Show help message",
    )

    # =============================
    # DETECCIÓN DE MODO EJECUCIÓN
    # =============================

    # Sin argumentos → mostrar info
    if len(sys.argv) == 1:
        print(info())
        sys.exit(0)

    # Si el primer argumento no es un subcomando conocido ni una flag,
    # asumimos modo ejecución directa
    first_arg = sys.argv[1]
    known_commands = {"transpile", "extract"}
    known_flags = {"--help", "-h", "--version"}

    if first_arg not in known_commands and first_arg not in known_flags:
        # Modo ejecución directa
        path = _resolve_entry_point(Path(first_arg))

        if not path.exists() or not path.is_file():
            print(f"Error: file not found: {path}")
            sys.exit(1)

        try:
            source = _transpile_to_memory(path)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        script_dir = str(path.parent.resolve())
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        globals_context = {
            "__name__": "__main__",
            "__file__": str(path.resolve()),
            "__builtins__": __builtins__,
        }

        exec(compile(source, str(path), "exec"), globals_context)
        return

    # Parsear argumentos normalmente para subcomandos
    args = parser.parse_args()

    # =============================
    # TRANSPILE
    # =============================
    if args.command == "transpile":
        path: Path = _resolve_entry_point(args.path)
        force: bool = args.force
        output: Path | None = args.output

        if not path.exists():
            print(f"Error: path not found: {path}")
            sys.exit(1)

        try:
            generated = transpile_tree(path, force=force, output_dir=output)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        for p in generated:
            print(p)

        return

    # =============================
    # EXTRACT
    # =============================
    if args.command == "extract":
        in_path: Path = args.input
        out_spec: Path = args.output

        if not in_path.exists() or not in_path.is_file():
            print(f"Error: file not found: {in_path}")
            sys.exit(1)

        # Determinar path de salida
        if out_spec.suffix:
            # Es un archivo específico: ./build/output.py
            out_path = out_spec
        else:
            # Es un directorio: ./build/ → ./build/input.py
            out_path = out_spec / in_path.with_suffix(".py").name

        try:
            tmp_py = _transpile_file(in_path, force=True)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

        # Crear directorio si no existe
        out_path.parent.mkdir(parents=True, exist_ok=True)

        out_path.write_text(
            tmp_py.read_text(encoding="utf-8"),
            encoding="utf-8",
        )

        print(out_path.resolve())
        return
