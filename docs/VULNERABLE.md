Vulnerabilidades de teste (para aulas)

Este arquivo descreve o código vulnerável presente em `vulnerable/app.py`.

Resumo:
- `vulnerable/app.py` contém a função `insecure_eval(user_input)` que usa
  `eval` diretamente na entrada do usuário — isso permite execução arbitrária
  de código e deve ser detectado pelas ferramentas de análise (CodeQL).
- Também há uma função `safe_eval_example(user_input)` com uma tentativa
  simples de filtragem para comparação didática (não é uma solução completa).

Como executar os testes localmente:
1. Instale as dependências do exercício:

```powershell
python -m pip install -r requirements.txt
```

2. Execute os testes com `pytest`:

```powershell
pytest -q
```

O objetivo é que o CodeQL detecte o uso inseguro de `eval` quando a workflow
for executada no GitHub Actions. Use este exemplo em sala para demonstrar:
- como o CodeQL reporta a vulnerabilidade;
- por que `eval` é perigoso;
- estratégias para mitigar (evitar `eval`, validação rigorosa, sandboxes).

AVISO: o código aqui é apenas para demonstração educacional. Não o use em
ambientes de produção nem em projetos reais sem correções apropriadas.
