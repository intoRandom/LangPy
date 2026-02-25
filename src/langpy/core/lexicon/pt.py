from .base import Lexicon


class PortugueseLexicon(Lexicon):
    language = "pt"

    table = {
        # controle de fluxo
        "se": "if",
        "senao": "else",
        "senaose": "elif",
        "enquanto": "while",
        "para": "for",
        "quebrar": "break",
        "continuar": "continue",
        "retornar": "return",
        "passar": "pass",
        "segundo": "match",
        "caso": "case",

        # operadores
        "e": "and",
        "ou": "or",
        "nao": "not",
        "em": "in",

        # estrutura
        "definir": "def",
        "classe": "class",
        "com": "with",
        "como": "as",
        "tentar": "try",
        "exceto": "except",
        "finalmente": "finally",
        "lancar": "raise",
        "global": "global",

        # exceções
        "Excecao": "Exception",

        # imports
        "importar": "import",
        "de": "from",

        # built-ins mínimos
        "imprimir": "print",
        "comprimento": "len",
        "tipo": "type",
        "intervalo": "range",
        "apagar": "del",
        "entrada": "input",
        "texto": "str",
        "inteiro": "int",
        "decimal": "float",
        "booleano": "bool",

        # booleanos
        "Verdadeiro": "True",
        "Falso": "False",
        "Nenhum": "None",
    }
