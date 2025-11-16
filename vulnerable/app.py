"""
Exemplo didático de vulnerabilidade OWASP Top 10 para CodeQL.

Este código contém apenas uma vulnerabilidade clássica de SQL In.
O objetivo é que o CodeQL detecte e a pipeline bloqueie o deploy para o
environment stage.
"""
import sqlite3


def build_query(usuario: str) -> str:
    """Constrói queries SQL de forma insegura (SQL Injection).

    Retorna três variantes inseguras para aumentar cobertura de detecção:
    1. f-string
    2. concatenação simples
    3. format()
    Qualquer uma delas permite injeção se `usuario` contiver payload malicioso.
    """
    q1 = f"SELECT * FROM users WHERE username = '{usuario}'"
    q2 = "SELECT * FROM users WHERE username = '" + usuario + "'"
    q3 = "SELECT * FROM users WHERE username = '{}'".format(usuario)
    # Retornamos a primeira apenas para uso didático, mas as outras são executadas no fluxo.
    return q1, q2, q3


def busca_usuario() -> None:
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, "
        "password TEXT)"
    )
    cur.execute(
        "INSERT INTO users (username, password) VALUES ('admin', 'admin123')"
    )
    usuario = input("Digite o nome de usuário: ")
    # Vulnerabilidade: SQL Injection (três padrões diferentes)
    q1, q2, q3 = build_query(usuario)

    for idx, q in enumerate([q1, q2, q3], start=1):
        print(f"[{idx}] Executando inseguramente: {q}")
        cur.execute(q)
        print(cur.fetchall())


if __name__ == "__main__":
    busca_usuario()
if __name__ == "__main__":
    busca_usuario()
