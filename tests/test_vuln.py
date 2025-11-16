import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from vulnerable import app


def test_build_query_basic():
    # Valida todas as variantes retornadas
    q1, q2, q3, q4, q5 = app.build_query("admin")
    expected = "SELECT * FROM users WHERE username = 'admin'"
    assert q1 == expected
    assert q2 == expected
    assert q3 == expected
    assert q4 == expected
    assert q5 == expected


def test_build_query_injection_pattern():
    payload = "teste' OR '1'='1"
    q1, q2, q3, q4, q5 = app.build_query(payload)
    for q in (q1, q2, q3, q4, q5):
        assert "OR '1'='1" in q
