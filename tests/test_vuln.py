import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from vulnerable import app


def test_build_command_basic():
    cmd = app.build_command("teste")
    assert cmd == "echo teste"


def test_build_command_injection_pattern():
    payload = "teste; uname -a"
    cmd = app.build_command(payload)
    # Apenas verifica se concatenou sem sanitização
    assert payload in cmd
