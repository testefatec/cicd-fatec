"""
Exemplo didático de vulnerabilidade OWASP Top 10 para CodeQL.

Este código contém uma vulnerabilidade clássica de SQL Injection.
O objetivo é que o CodeQL detecte e a pipeline bloqueie o deploy para o stage.
"""

import sqlite3

def busca_usuario():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cur.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    usuario = input("Digite o nome de usuário: ")
    # Vulnerabilidade: SQL Injection
    query = f"SELECT * FROM users WHERE username = '{usuario}'"
    print(f"Executando: {query}")
    cur.execute(query)
    print(cur.fetchall())

if __name__ == "__main__":
    busca_usuario()
