"""
Exemplos intencionalmente vulneráveis para fins didáticos.

AVISO: Este código é inseguro por design. Não use em produção.

Objetivo: demonstrar vulnerabilidades simples que o CodeQL deve detectar
 (ex.: uso de `eval` com entrada do usuário e command injection).
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
    # Implementação simples e limitada — não execute em produção
    # sem revisão.
    allowed_chars = "0123456789+-*/(). "
    if any(c not in allowed_chars for c in user_input):
        raise ValueError("Entrada contém caracteres não permitidos")
    return eval(user_input)


def insecure_eval_from_input():
    """Exemplo ainda mais perigoso: lê entrada do usuário e avalia diretamente.

    Este fluxo deve ser detectado como potencialmente explorável
    pois a origem é `input()` (não confiável) e o destino é
    `eval()` (código dinâmico).
    """
    expr = input("Digite uma expressão: ")
    return eval(expr)


def insecure_command_from_input():
    """Command injection: executa comando fornecido pelo usuário com shell=True.

    Exemplo didático para demonstrar como entradas não confiáveis
    podem levar à execução de comandos arbitrários no sistema
    operacional.
    """
    import subprocess

    cmd = input("Digite um comando: ")
    # shell=True com entrada não sanitizada é perigoso
    subprocess.run(cmd, shell=True)


def insecure_yaml_load():
    """Deserialização YAML insegura usando yaml.load sem SafeLoader.

    Leitura de dados YAML não confiáveis pode executar objetos arbitrários
    dependendo do Loader. Use yaml.safe_load em produção.
    """
    import yaml

    data = input("Digite YAML: ")
    # Uso inseguro: yaml.load sem especificar SafeLoader
    return yaml.load(data)


def insecure_pickle_load():
    """Deserialização de entrada não confiável com pickle.loads.

    Deserializar dados fornecidos por usuário permite execução de código
    arbitrário. Não use pickle com dados não confiáveis.
    """
    import pickle

    blob = input("Digite dados pickle (string): ")
    # Inseguro: desserializa entrada não confiável
    return pickle.loads(blob)  # type: ignore[arg-type]
