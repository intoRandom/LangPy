from __future__ import annotations

from pathlib import Path
from typing import List, Set
import shutil

from .imports import parse_imports
from .resolver import resolve_import_event
from .transpiler import _transpile_file


def _ensure_within_root(path: Path, root: Path) -> None:
    try:
        path.relative_to(root)
    except ValueError:
        raise RuntimeError(f"Import escapes root directory: {path}")


def transpile_tree(
    entry_path: Path,
    *,
    force: bool = False,
    output_dir: Path | None = None,  # NUEVO
) -> List[Path]:

    if not entry_path.exists() or not entry_path.is_file():
        raise FileNotFoundError(entry_path)

    entry_path = entry_path.resolve()
    root_dir = entry_path.parent

    search_paths = [root_dir]

    pending: list[Path] = [entry_path]
    processed: set[Path] = set()
    generated: list[Path] = []
    # NUEVO: rastrear .py vanilla encontrados
    vanilla_py_files: set[Path] = set()

    while pending:
        current = pending.pop()

        if current in processed:
            continue

        _ensure_within_root(current, root_dir)

        # Calcular output path si output_dir está especificado
        if output_dir:
            rel_path = current.relative_to(root_dir)
            output_path = output_dir / rel_path.with_suffix(".py")
        else:
            output_path = None

        # 1. transpilar archivo actual
        output_py = _transpile_file(
            current, force=force, output_path=output_path)
        generated.append(output_py)

        # 2. parsear imports del .py generado
        python_source = output_py.read_text(encoding="utf-8")
        events = parse_imports(python_source)

        # 3. resolver imports
        for event in events:
            resolved = resolve_import_event(
                event,
                current_file=current,
                root_dir=root_dir,
                search_paths=search_paths,
            )

            for path in resolved:
                if path not in processed:
                    pending.append(path)

        # 4. NUEVO: detectar archivos .py vanilla que sean imports
        if output_dir:
            for event in events:
                modules: list[str] = []

                if event.is_from:
                    if event.module:
                        modules.append(event.module)
                else:
                    modules.extend(event.names)

                for module in modules:
                    parts = module.split(".")

                    # Buscar desde current_file o search_paths
                    if event.level > 0:
                        base = current.parent
                        for _ in range(event.level - 1):
                            base = base.parent
                        candidates = [base]
                    else:
                        candidates = search_paths

                    for base in candidates:
                        pkg_path = base.joinpath(*parts)

                        # Archivo .py directo
                        py_file = pkg_path.with_suffix(".py")
                        if py_file.exists() and py_file.is_file():
                            try:
                                _ensure_within_root(py_file, root_dir)
                                vanilla_py_files.add(py_file.resolve())
                            except RuntimeError:
                                pass

                        # Paquete __init__.py
                        init_py = pkg_path / "__init__.py"
                        if init_py.exists() and init_py.is_file():
                            try:
                                _ensure_within_root(init_py, root_dir)
                                vanilla_py_files.add(init_py.resolve())
                            except RuntimeError:
                                pass

        processed.add(current)

    # 5. NUEVO: copiar archivos .py vanilla si output_dir está especificado
    if output_dir:
        for vanilla_file in vanilla_py_files:
            rel_path = vanilla_file.relative_to(root_dir)
            dest = output_dir / rel_path

            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(vanilla_file, dest)
            generated.append(dest)

    return generated
