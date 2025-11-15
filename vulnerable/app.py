"""
Exemplos intencionalmente vulneráveis para fins didáticos.

AVISO: Este código é inseguro por design. Não use em produção.

Objetivo: demonstrar vulnerabilidades simples que o CodeQL deve detectar
 (ex.: uso de `eval` com entrada do usuário).
"""

def insecure_eval(user_input: str):
    """Avalia uma expressão a partir de uma string fornecida pelo usuário.

    Vulnerabilidade: usar `eval` em entrada não confiável permite execução
    arbitrária de código. Este é um exemplo didático para ser detectado pelo
    CodeQL e discutido em sala de aula.
    """
    return eval(user_input)


def safe_eval_example(user_input: str):
    """Exemplo seguro: avalia apenas expressões numéricas simples.

    Implementado apenas para comparação com a função insegura.
    """
    # Implementação simples e limitada — não execute em produção sem revisão.
    allowed_chars = "0123456789+-*/(). "
    if any(c not in allowed_chars for c in user_input):
        raise ValueError("Entrada contém caracteres não permitidos")
    return eval(user_input)
