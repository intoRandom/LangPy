import sys
import subprocess
from pathlib import Path


def run_langpy(*args, cwd):
    return subprocess.run(
        [sys.executable, "-m", "langpy", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )

# --- Tests de Conflictos y Errores ---


def test_output_and_transpile_conflict(tmp_path):
    """Verifica que no se pueden usar extract y transpile al mismo tiempo."""
    # CAMBIO: Este test ya no aplica porque son subcomandos mutuamente exclusivos
    # argparse previene esto automáticamente. Podemos eliminarlo o cambiar el test:

    (tmp_path / "a.pyes").write_text("imprimir('x')", encoding="utf-8")

    # Intentar usar dos subcomandos a la vez es sintácticamente inválido
    # argparse rechazará esto antes de llegar a tu lógica
    result = run_langpy("extract", "a.pyes", "transpile",
                        "a.pyes", cwd=tmp_path)

    assert result.returncode != 0
    # argparse mostrará error de uso inválido
    error_msg = (result.stdout + result.stderr).lower()
    assert "usage:" in error_msg or "error" in error_msg


def test_unsupported_extension(tmp_path):
    """Verifica que el compilador falle con extensiones no soportadas."""
    (tmp_path / "a.txt").write_text("hola", encoding="utf-8")

    result = run_langpy("a.txt", cwd=tmp_path)

    assert result.returncode != 0
    # SIN CAMBIOS - este test sigue siendo válido


# --- Tests Previos (Actualizados a subcomandos) ---


def test_extract_single_file(tmp_path):  # RENOMBRADO: output -> extract
    """Verifica que extract genere un archivo en la ubicación especificada."""
    (tmp_path / "main.pyes").write_text("imprimir('hola')", encoding="utf-8")

    out_file = tmp_path / "build" / "main.py"

    # CAMBIO: usar subcomando 'extract' con flag -o
    result = run_langpy("extract", "main.pyes", "-o",
                        str(out_file), cwd=tmp_path)

    assert result.returncode == 0
    assert out_file.exists()
    assert "print('hola')" in out_file.read_text(encoding="utf-8")


def test_extract_to_directory(tmp_path):
    """Verifica que extract genere archivo en directorio con nombre automático."""
    (tmp_path / "main.pyes").write_text("imprimir('hola')", encoding="utf-8")

    build_dir = tmp_path / "build"
    build_dir.mkdir()

    # NUEVO TEST: extract con directorio (debería crear build/main.py)
    result = run_langpy("extract", "main.pyes", "-o",
                        str(build_dir), cwd=tmp_path)

    assert result.returncode == 0
    out_file = build_dir / "main.py"
    assert out_file.exists()
    assert "print('hola')" in out_file.read_text(encoding="utf-8")


def test_transpile_single_file(tmp_path):
    """Verifica que transpile genere archivo .py al lado del .pyes"""
    (tmp_path / "main.pyes").write_text("imprimir('hola')", encoding="utf-8")

    # CAMBIO: usar subcomando 'transpile'
    result = run_langpy("transpile", "main.pyes", cwd=tmp_path)

    assert result.returncode == 0
    out_file = tmp_path / "main.py"
    assert out_file.exists()
    assert "print('hola')" in out_file.read_text(encoding="utf-8")


def test_transpile_with_output_dir(tmp_path):
    """Verifica que transpile con --output copie a directorio especificado."""
    (tmp_path / "main.pyes").write_text("imprimir('hola')", encoding="utf-8")

    dist_dir = tmp_path / "dist"

    # NUEVO TEST: transpile con --output
    result = run_langpy("transpile", "main.pyes", "-o",
                        str(dist_dir), cwd=tmp_path)

    assert result.returncode == 0
    out_file = dist_dir / "main.py"
    assert out_file.exists()
    assert "print('hola')" in out_file.read_text(encoding="utf-8")
