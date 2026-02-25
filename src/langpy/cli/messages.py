def info() -> str:
    return (
        "LangPy — Lexical layer for Python\n\n"
        "Write Python using your native-language keywords.\n\n"
        "Supported languages:\n"
        "  .pyes  Spanish\n"
        "  .pypt  Portuguese\n"
        "  .pyfr  French\n\n"
        "Run `langpy --help` for usage."
    )


def help() -> str:
    return (
        "Usage:\n"
        "  langpy <file/dir>                          Execute a LangPy file\n"
        "  langpy transpile <file/dir> [options]      Transpile with imports resolution\n"
        "  langpy extract <file> -o <output>          Transpile single file (dev/tooling)\n\n"
        "Options:\n"
        "  -h, --help                Show this help message and exit\n"
        "  --version                 Print package version and exit\n\n"
        "Transpile Options:\n"
        "  -f, --force               Overwrite existing .py files\n"
        "  -o, --output <dir>        Output directory for transpiled files\n\n"
        "Extract Options:\n"
        "  -o, --output <path>       Output file or directory (required)\n\n"
        "Examples:\n"
        "  langpy main.pyes                           # Execute directly\n"
        "  langpy ./directory/                        # Require __main__ file\n"
        "  langpy transpile main.pypt                 # Transpile in same directory\n"
        "  langpy transpile main.pypt -f -o dist      # Transpile to dist/ folder\n"
        "  langpy transpile ./directory/              # Require __main__ file\n"
        "  langpy extract input.pyfr -o build/        # Extract to build/input.py\n"
        "  langpy extract input.pypt -o out.py        # Extract to out.py\n\n"
        "Note:\n"
        "  'extract' is intended for development tools and IDE integrations only."
    )
