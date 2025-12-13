from pyes.core.transpiler import transpile
from pyes.core.lexicon.es import SpanishLexicon


def test_attributes_not_translated():
    source = "obj.imprimir()"
    expected = "obj.imprimir()"

    result = transpile(source, SpanishLexicon())

    assert result == expected
