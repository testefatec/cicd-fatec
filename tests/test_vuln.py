import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vulnerable import app


def test_build_query_basic():
    # Gera a query com o nome fornecido
    q = app.build_query("admin")
    assert q == "SELECT * FROM users WHERE username = 'admin'"


def test_build_query_injection_pattern():
    # Demonstra a concatenação insegura (vulnerável a SQLi)
    payload = "teste' OR '1'='1"
    q = app.build_query(payload)
    assert "OR '1'='1" in q
