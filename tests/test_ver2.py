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


# ========================================
# Tests: Ejecución directa con directorios
# ========================================

def test_run_directory_with_main_pyes(tmp_path):
    """Ejecuta directorio que contiene __main__.pyes"""
    project = tmp_path / "proyecto"
    project.mkdir()
    (project / "__main__.pyes").write_text("imprimir('desde main')", encoding="utf-8")

    result = run_langpy(str(project), cwd=tmp_path)

    assert result.returncode == 0
    assert "desde main" in result.stdout


def test_run_directory_with_main_pypt(tmp_path):
    """Ejecuta directorio con __main__.pypt (portugués)"""
    project = tmp_path / "projeto"
    project.mkdir()
    (project / "__main__.pypt").write_text("imprimir('olá')", encoding="utf-8")

    result = run_langpy(str(project), cwd=tmp_path)

    assert result.returncode == 0
    assert "olá" in result.stdout


def test_run_directory_with_main_pyfr(tmp_path):
    """Ejecuta directorio con __main__.pyfr (francés)"""
    project = tmp_path / "projet"
    project.mkdir()
    (project / "__main__.pyfr").write_text("imprimer('bonjour')", encoding="utf-8")

    result = run_langpy(str(project), cwd=tmp_path)

    assert result.returncode == 0
    assert "bonjour" in result.stdout


def test_run_directory_without_main_fails(tmp_path):
    """Error cuando directorio no tiene __main__"""
    project = tmp_path / "empty"
    project.mkdir()
    (project / "other.pyes").write_text("imprimir('x')", encoding="utf-8")

    result = run_langpy(str(project), cwd=tmp_path)

    assert result.returncode != 0
    assert "must contain __main__" in (result.stdout + result.stderr).lower()


def test_run_directory_prefers_pyes_over_others(tmp_path):
    """Si hay múltiples __main__.{ext}, prefiere .pyes"""
    project = tmp_path / "multi"
    project.mkdir()
    (project / "__main__.pyes").write_text("imprimir('español')", encoding="utf-8")
    (project / "__main__.pypt").write_text("imprimir('português')", encoding="utf-8")

    result = run_langpy(str(project), cwd=tmp_path)

    assert result.returncode == 0
    assert "español" in result.stdout


# ========================================
# Tests: Transpile con directorios
# ========================================

def test_transpile_directory_with_main(tmp_path):
    """Transpila directorio que contiene __main__.pyes"""
    project = tmp_path / "app"
    project.mkdir()
    (project / "__main__.pyes").write_text("imprimir('app')", encoding="utf-8")

    result = run_langpy("transpile", str(project), cwd=tmp_path)

    assert result.returncode == 0
    assert (project / "__main__.py").exists()
    assert "print('app')" in (
        project / "__main__.py").read_text(encoding="utf-8")


def test_transpile_directory_without_main_fails(tmp_path):
    """Error al transpilar directorio sin __main__"""
    project = tmp_path / "incomplete"
    project.mkdir()
    (project / "utils.pyes").write_text("imprimir('util')", encoding="utf-8")

    result = run_langpy("transpile", str(project), cwd=tmp_path)

    assert result.returncode != 0
    assert "must contain __main__" in (result.stdout + result.stderr).lower()


# ========================================
# Tests: Transpile con --output
# ========================================

def test_transpile_with_output_single_file(tmp_path):
    """Transpila archivo único a directorio específico"""
    (tmp_path / "main.pyes").write_text("imprimir('test')", encoding="utf-8")

    dist = tmp_path / "dist"
    result = run_langpy("transpile", "main.pyes",
                        "-o", str(dist), cwd=tmp_path)

    assert result.returncode == 0
    assert (dist / "main.py").exists()
    assert "print('test')" in (dist / "main.py").read_text(encoding="utf-8")


def test_transpile_with_output_preserves_structure(tmp_path):
    """Transpila preservando estructura de directorios"""
    # Estructura:
    # main.pyes
    # utils/helper.pyes

    (tmp_path / "main.pyes").write_text("desde .utils.helper importar ayuda", encoding="utf-8")

    utils = tmp_path / "utils"
    utils.mkdir()
    (utils / "helper.pyes").write_text("def ayuda(): pasar", encoding="utf-8")

    dist = tmp_path / "dist"
    result = run_langpy("transpile", "main.pyes",
                        "-o", str(dist), cwd=tmp_path)

    assert result.returncode == 0
    assert (dist / "main.py").exists()
    assert (dist / "utils" / "helper.py").exists()


def test_transpile_with_output_copies_vanilla_py(tmp_path):
    """Transpila y copia archivos .py vanilla referenciados"""
    # main.pyes importa vanilla.py
    (tmp_path / "main.pyes").write_text("desde vanilla importar func", encoding="utf-8")
    (tmp_path / "vanilla.py").write_text("def func(): pass", encoding="utf-8")

    dist = tmp_path / "dist"
    result = run_langpy("transpile", "main.pyes",
                        "-o", str(dist), cwd=tmp_path)

    assert result.returncode == 0
    assert (dist / "main.py").exists()
    assert (dist / "vanilla.py").exists()
    assert "def func(): pass" in (dist / "vanilla.py").read_text(encoding="utf-8")


def test_transpile_with_output_respects_force(tmp_path):
    """--output respeta flag --force"""
    (tmp_path / "main.pyes").write_text("imprimir('nuevo')", encoding="utf-8")

    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "main.py").write_text("print('viejo')", encoding="utf-8")

    # Sin --force debería fallar
    result = run_langpy("transpile", "main.pyes",
                        "-o", str(dist), cwd=tmp_path)
    assert result.returncode != 0

    # Con --force debería sobrescribir
    result = run_langpy("transpile", "main.pyes", "-o",
                        str(dist), "-f", cwd=tmp_path)
    assert result.returncode == 0
    assert "print('nuevo')" in (dist / "main.py").read_text(encoding="utf-8")


# ========================================
# Tests: Extract (modo tooling)
# ========================================

def test_extract_to_file(tmp_path):
    """Extract genera archivo en ubicación específica"""
    (tmp_path / "source.pyes").write_text("imprimir('data')", encoding="utf-8")

    out = tmp_path / "output.py"
    result = run_langpy("extract", "source.pyes", "-o", str(out), cwd=tmp_path)

    assert result.returncode == 0
    assert out.exists()
    assert "print('data')" in out.read_text(encoding="utf-8")


def test_extract_to_directory(tmp_path):
    """Extract a directorio usa nombre automático"""
    (tmp_path / "app.pyes").write_text("imprimir('app')", encoding="utf-8")

    build = tmp_path / "build"
    build.mkdir()

    result = run_langpy("extract", "app.pyes", "-o", str(build), cwd=tmp_path)

    assert result.returncode == 0
    assert (build / "app.py").exists()
    assert "print('app')" in (build / "app.py").read_text(encoding="utf-8")


def test_extract_creates_parent_directories(tmp_path):
    """Extract crea directorios padres automáticamente"""
    (tmp_path / "file.pyes").write_text("imprimir('ok')", encoding="utf-8")

    nested = tmp_path / "a" / "b" / "c" / "output.py"
    result = run_langpy("extract", "file.pyes", "-o",
                        str(nested), cwd=tmp_path)

    assert result.returncode == 0
    assert nested.exists()


def test_extract_ignores_imports(tmp_path):
    """Extract NO transpila dependencias (modo single-file)"""
    (tmp_path / "main.pyes").write_text("desde helper importar func", encoding="utf-8")
    (tmp_path / "helper.pyes").write_text("def func(): pasar", encoding="utf-8")

    out = tmp_path / "output.py"
    result = run_langpy("extract", "main.pyes", "-o", str(out), cwd=tmp_path)

    assert result.returncode == 0
    assert out.exists()
    # helper.py NO debe haberse generado
    assert not (tmp_path / "helper.py").exists()


# ========================================
# Tests: Abreviaciones
# ========================================

def test_short_flags_work(tmp_path):
    """Verifica que -f y -o funcionen"""
    (tmp_path / "test.pyes").write_text("imprimir('x')", encoding="utf-8")
    (tmp_path / "test.py").write_text("old", encoding="utf-8")

    # -f para force
    result = run_langpy("transpile", "test.pyes", "-f", cwd=tmp_path)
    assert result.returncode == 0

    # -o para output
    dist = tmp_path / "dist"
    result = run_langpy("transpile", "test.pyes", "-o",
                        str(dist), "-f", cwd=tmp_path)
    assert result.returncode == 0
    assert (dist / "test.py").exists()
