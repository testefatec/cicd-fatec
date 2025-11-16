"""
Exemplo didático de vulnerabilidade OWASP Top 10 para CodeQL.

Este código contém apenas uma vulnerabilidade clássica de SQL In.
O objetivo é que o CodeQL detecte e a pipeline bloqueie o deploy para o
environment stage.
"""
import sqlite3


def build_query(usuario: str) -> str:
    """Constrói uma query SQL de forma insegura (SQL Injection).

    Vulnerabilidade: interpolação direta de entrada não confiável na query.
    """
    return f"SELECT * FROM users WHERE username = '{usuario}'"


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
    # Vulnerabilidade: SQL Injection
    query = build_query(usuario)
    print(f"Executando: {query}")
    cur.execute(query)
    print(cur.fetchall())


if __name__ == "__main__":
    busca_usuario()
if __name__ == "__main__":
    busca_usuario()
