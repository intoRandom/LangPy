from .base import Lexicon


class SpanishLexicon(Lexicon):
    language = "es"

    table = {
        # control de flujo
        "si": "if",
        "sino": "else",
        "sisi": "elif",
        "mientras": "while",
        "para": "for",
        "romper": "break",
        "continuar": "continue",
        "retornar": "return",
        "pasar": "pass",
        "segun": "match",
        "caso": "case",

        # operadores
        "y": "and",
        "o": "or",
        "no": "not",
        "en": "in",

        # estructura
        "definir": "def",
        "clase": "class",
        "con": "with",
        "como": "as",
        "intentar": "try",
        "excepto": "except",
        "finalmente": "finally",
        "lanzar": "raise",
        "global": "global",

        # excepciones
        "Excepcion": "Exception",

        # imports
        "importar": "import",
        "desde": "from",

        # built-ins mínimos
        "imprimir": "print",
        "longitud": "len",
        "tipo": "type",
        "rango": "range",
        "borrar": "del",
        "entrada": "input",
        "texto": "str",
        "entero": "int",
        "decimal": "float",
        "booleano": "bool",

        # booleanos
        "Verdadero": "True",
        "Falso": "False",
        "Ninguno": "None",
    }
