# Material Didático: Vulnerabilidades de Segurança em Python

## Slide 1: Introdução

**Objetivo**: Entender vulnerabilidades comuns em Python e como o CodeQL as detecta.

Neste material, exploramos:
1. **Uso inseguro de `eval`** — execução arbitrária de código
2. **Por que é perigoso** — impacto e consequências
3. **Como corrigir** — práticas seguras e alternativas

---

## Slide 2: Vulnerabilidade #1 – `eval` com entrada não confiável

### O Problema (Código Vulnerável)

```python
def insecure_eval(user_input: str):
    """Executa qualquer código Python fornecido pelo usuário."""
    return eval(user_input)

# Uso
resultado = insecure_eval(input("Digite uma expressão: "))
```

### Por que é perigoso?

- **Execução arbitrária de código**: um atacante pode executar qualquer comando Python.
- **Exemplo de ataque**:
  ```python
  # Entrada do atacante:
  "__import__('os').system('rm -rf /')"
  # Resultado: delete de arquivos!
  
  # Ou roubo de dados:
  "__import__('os').getenv('DATABASE_PASSWORD')"
  ```
- **Impacto**: comprometimento completo do sistema, roubo de dados, ransomware.

### Cenários perigosos

| Cenário | Risco |
|---------|-------|
| API que aceita expressões de usuários | Ataque remoto |
| Formulário web que avalia entrada | Acesso não autorizado |
| Cálculo de fórmulas personalizadas | Roubo de informações sensíveis |

---

## Slide 3: Como corrigir – Alternativas seguras a `eval`

### Opção 1: Use uma biblioteca segura (RECOMENDADO)

```python
from ast import literal_eval

def safe_eval_literal(user_input: str):
    """Avalia apenas literais Python (strings, números, listas, etc.)."""
    try:
        return literal_eval(user_input)
    except (ValueError, SyntaxError):
        raise ValueError("Entrada inválida")

# Exemplos seguros:
print(safe_eval_literal("42"))              # ✓ OK: 42
print(safe_eval_literal("[1, 2, 3]"))       # ✓ OK: [1, 2, 3]
print(safe_eval_literal("'hello'"))         # ✓ OK: 'hello'

# Exemplos rejeitados (seguro!):
safe_eval_literal("__import__('os')")       # ✗ ValueError
safe_eval_literal("os.system('ls')")        # ✗ ValueError
```

**Vantagens**: bloqueia automaticamente chamadas de funções e imports.

### Opção 2: Use `ast.literal_eval` com validação

```python
from ast import literal_eval

def safe_math_eval(user_input: str):
    """Avalia apenas expressões matemáticas simples."""
    allowed_chars = "0123456789+-*/(). "
    
    # Valida caracteres
    if any(c not in allowed_chars for c in user_input):
        raise ValueError("Caracteres não permitidos")
    
    # Rejeita múltiplas operações perigosas
    if any(keyword in user_input.lower() for keyword in ['import', 'lambda', '__']):
        raise ValueError("Operação não permitida")
    
    # Usa literal_eval para segurança extra
    try:
        return eval(compile(user_input, '<string>', 'eval'), 
                   {"__builtins__": {}})  # Limita builtins
    except Exception as e:
        raise ValueError(f"Erro ao avaliar: {e}")

# Exemplos:
print(safe_math_eval("2 + 3"))              # ✓ OK: 5
print(safe_math_eval("(10 * 5) - 3"))       # ✓ OK: 47
print(safe_math_eval("__import__('os')"))   # ✗ ValueError
```

### Opção 3: Use uma biblioteca dedicada

```python
# Usando 'numexpr' para expressões numéricas seguras
import numexpr

def safe_numeric_eval(user_input: str):
    """Avalia expressões numéricas com segurança."""
    try:
        result = numexpr.evaluate(user_input)
        return result
    except Exception as e:
        raise ValueError(f"Expressão inválida: {e}")

# Exemplos:
print(safe_numeric_eval("2 + 3 * 4"))       # ✓ OK: 14
print(safe_numeric_eval("sqrt(16)"))        # ✓ OK: 4.0
```

**Instalação**: `pip install numexpr`

---

## Slide 4: Resumo – Boas práticas de segurança

### Regra de Ouro 🔒

**NUNCA use `eval`, `exec` ou `compile` com entrada não confiável.**

### Checklist de Segurança

- [ ] **Identificar entrada não confiável** — formulários, APIs, arquivos, variáveis de ambiente.
- [ ] **Usar alternativas seguras** — `literal_eval`, `numexpr`, bibliotecas validadas.
- [ ] **Validar entrada** — whitelist de caracteres, comprimento máximo, tipos esperados.
- [ ] **Usar ferramentas de análise** — CodeQL, Bandit, SonarQube detectam essas vulnerabilidades.
- [ ] **Testar casos de ataque** — tente quebrar seu próprio código!

### Código Seguro vs. Inseguro

| Inseguro ❌ | Seguro ✓ |
|------------|----------|
| `eval(user_input)` | `literal_eval(user_input)` |
| `exec(code)` | validação + `ast.literal_eval` |
| `compile(user_input, ...)` | biblioteca dedicada (numexpr, etc.) |
| Sem validação | Whitelist de caracteres |

---

## Slide 5: Atividade prática para alunos

### Exercício 1: Identifique a vulnerabilidade

```python
def calculate(expression: str):
    result = eval(expression)  # O que está errado aqui?
    return result
```

**Resposta esperada**: uso direto de `eval` com entrada do usuário permite execução de código arbitrário.

### Exercício 2: Corrija o código

```python
# ANTES (vulnerável):
def calculate(expression: str):
    return eval(expression)

# DEPOIS (seguro):
from ast import literal_eval

def calculate(expression: str):
    allowed_chars = "0123456789+-*/(). "
    if any(c not in allowed_chars for c in expression):
        raise ValueError("Caracteres não permitidos")
    
    try:
        return eval(compile(expression, '<string>', 'eval'),
                   {"__builtins__": {}})
    except Exception as e:
        raise ValueError(f"Expressão inválida: {e}")
```

### Exercício 3: Teste a segurança

```python
# Teste com entrada maliciosa:
try:
    calculate("__import__('os').system('ls')")
    print("❌ FALHOU: Código foi executado!")
except ValueError as e:
    print(f"✓ OK: {e}")
```

---

## Slide 6: Como o CodeQL detecta isso?

### O que o CodeQL procura

1. **Padrão `eval(...)`** — detecta todas as chamadas a `eval`.
2. **Origem da entrada** — rastreia se a origem é não confiável (user input, request, etc.).
3. **Sem validação** — verifica se há filtros ou validação antes do `eval`.

### Exemplo de detecção

```python
# CodeQL DETECTA isto ⚠️
def vulnerable_function(user_input):
    return eval(user_input)  # CWE-95: Improper Neutralization of Directives

# CodeQL IGNORA isto (com segurança)
def safe_function(user_input):
    return literal_eval(user_input)  # Seguro
```

### Como ver os resultados no GitHub

1. Faça um push com código vulnerável.
2. Vá em `Security` → `Code scanning alerts`.
3. Veja a vulnerabilidade reportada com severidade.
4. Clique para ver as recomendações.

---

## Slide 7: Recursos e referências

### Leitura adicional

- [OWASP – Code Injection](https://owasp.org/www-community/attacks/Code_Injection)
- [CWE-95: Improper Neutralization of Directives in Dynamically Evaluated Code](https://cwe.mitre.org/data/definitions/95.html)
- [Python `ast.literal_eval` documentation](https://docs.python.org/3/library/ast.html#ast.literal_eval)

### Ferramentas de análise

- **CodeQL** — análise estática (GitHub Advanced Security)
- **Bandit** — scanner de segurança Python específico
- **SonarQube** — análise contínua de qualidade e segurança

### Exercícios propostos

1. Execute a workflow CI/CD com o arquivo `vulnerable/app.py` e observe o CodeQL detectar a vulnerabilidade.
2. Corrija o código em `vulnerable/app.py` e veja a pipeline passar.
3. Implemente sua própria função segura de cálculo em uma nova branch.

---

## Conclusão

A segurança é essencial em desenvolvimento de software. Use CodeQL e outras ferramentas para
identificar e corrigir vulnerabilidades **antes** de fazer deploy em produção.

**Lembre-se**: um código inseguro hoje pode ser um ataque bem-sucedido amanhã! 🔒
