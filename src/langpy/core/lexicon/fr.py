from .base import Lexicon


class FrenchLexicon(Lexicon):
    language = "fr"

    table = {
        # contrôle de flux
        "si": "if",
        "sinon": "else",
        "sinonsi": "elif",
        "tantque": "while",
        "pour": "for",
        "rompre": "break",
        "continuer": "continue",
        "retourner": "return",
        "passer": "pass",
        "selon": "match",
        "cas": "case",

        # opérateurs
        "et": "and",
        "ou": "or",
        "non": "not",
        "dans": "in",

        # structure
        "definir": "def",
        "classe": "class",
        "avec": "with",
        "comme": "as",
        "essayer": "try",
        "excepte": "except",
        "finalement": "finally",
        "lancer": "raise",
        "global": "global",

        # exceptions
        "Exception": "Exception",

        # imports
        "importer": "import",
        "depuis": "from",

        # built-ins mínimos
        "imprimer": "print",
        "longueur": "len",
        "type": "type",
        "intervalle": "range",
        "supprimer": "del",
        "entree": "input",
        "texte": "str",
        "entier": "int",
        "decimal": "float",
        "booleen": "bool",

        # booléens
        "Vrai": "True",
        "Faux": "False",
        "Aucun": "None",
    }
