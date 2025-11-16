"""Exemplo didático de vulnerabilidade OWASP Top 10 (SQL Injection).

Objetivo: fornecer múltiplos padrões inseguros de construção de query para
facilitar a detecção por CodeQL e bloquear o deploy na pipeline.
"""
import sqlite3


def build_query(usuario: str) -> tuple[str, str, str, str, str]:
        """Constrói múltiplas variantes inseguras de consulta.

        Variantes retornadas:
            1. f-string
            2. concatenação com +
            3. format()
            4. old-style % formatting
            5. join() sobre lista
        Todas interpolam diretamente a entrada não confiável.
        """
        q1 = f"SELECT * FROM users WHERE username = '{usuario}'"
        q2 = "SELECT * FROM users WHERE username = '" + usuario + "'"
        q3 = "SELECT * FROM users WHERE username = '{}'".format(usuario)
        q4 = "SELECT * FROM users WHERE username = '%s'" % usuario
        q5 = "".join(["SELECT * FROM users WHERE username = '", usuario, "'"])
        return q1, q2, q3, q4, q5


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
    # Vulnerabilidade: SQL Injection (cinco padrões diferentes)
    q1, q2, q3, q4, q5 = build_query(usuario)

    for idx, q in enumerate([q1, q2, q3, q4, q5], start=1):
        print(f"[{idx}] Executando inseguramente: {q}")
        cur.execute(q)
        print(cur.fetchall())


if __name__ == "__main__":
    busca_usuario()
