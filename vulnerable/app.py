"""Exemplo didático: OWASP Top 10 - Command Injection.

Objetivo: demonstrar um fluxo simples que o CodeQL costuma detectar
(comando vindo de `input()` e executado com `shell=True`).
Mantém apenas UMA vulnerabilidade clara para a aula.
"""
import os
import subprocess


def build_command(user_input: str) -> str:
    """Constrói um comando sem sanitização (vulnerável a injection)."""
    return f"echo {user_input}"


def run_insecure_command() -> None:
    cmd = input("Digite um comando para executar: ")
    full = build_command(cmd)
    # Vuln: comm injection (ent. não confiável em shell=True e os.system)
    print(f"Executando inseguramente: {full}")
    os.system(full)
    subprocess.run(full, shell=True)


if __name__ == "__main__":
    run_insecure_command()
