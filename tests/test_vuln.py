import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vulnerable import app


def test_build_query_basic():
    # Gera variantes inseguras; valida a primeira
    q1, q2, q3 = app.build_query("admin")
    assert q1 == "SELECT * FROM users WHERE username = 'admin'"
    assert q2 == "SELECT * FROM users WHERE username = 'admin'"
    assert q3 == "SELECT * FROM users WHERE username = 'admin'"


def test_build_query_injection_pattern():
    payload = "teste' OR '1'='1"
    q1, q2, q3 = app.build_query(payload)
    assert "OR '1'='1" in q1
    assert "OR '1'='1" in q2
    assert "OR '1'='1" in q3
