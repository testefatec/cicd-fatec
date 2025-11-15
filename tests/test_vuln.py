from vulnerable import app


def test_insecure_eval_numeric():
    # Avalia expressão numérica simples
    assert app.insecure_eval("1+2") == 3


def test_insecure_eval_string_concat():
    # Avalia concatenação de strings
    assert app.insecure_eval("'a' + 'b'") == 'ab'


def test_safe_eval_rejects_bad_chars():
    try:
        app.safe_eval_example("__import__('os').system('echo no')")
        # se não lançar, falha o teste
        assert False
    except ValueError:
        assert True
