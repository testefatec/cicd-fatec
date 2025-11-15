# cicd-fatec

Este repositório contém um exemplo didático de pipeline CI/CD para projetos Python
com validação de segurança usando CodeQL (GitHub Advanced Security). O objetivo é
fornecer um pipeline curto, comentado e fácil de entender para uso em sala de aula.

**Arquivos principais**:
- `/.github/workflows/ci-cd-python.yml`: workflow do GitHub Actions com CodeQL,
	lint/tests e um passo de deploy para *stage* (placeholder).

**Visão rápida**:
- Ao enviar um push ou abrir uma pull request para `main`, a workflow dispara.
- O CodeQL roda e, se encontrar vulnerabilidades de severidade >= *medium*, a
	pipeline falha e gera alertas.
- Se CodeQL e os testes/lint passarem, o job de *deploy-stage* será executado.

**Como usar (rápido)**:
1. Abra o repositório no GitHub.
2. Habilite o GitHub Advanced Security (Code Scanning) no repositório (se disponível).
3. Ajuste `/.github/workflows/ci-cd-python.yml` conforme sua infra de deploy real.

**Configurar secrets para deploy (exemplo)**:
- `STAGE_HOST`: host do servidor de stage
- `STAGE_USER`: usuário SSH
- `STAGE_KEY`: chave privada SSH (considere usar GitHub Encrypted Secrets)
 - `STAGE_TARGET`: diretório remoto onde os arquivos serão copiados (ex.: `/var/www/stage-app/`)

**Onde editar a regra de falha do CodeQL**:
- No arquivo `/.github/workflows/ci-cd-python.yml`, a opção `fail-on` está
	configurada como `medium`. Para falhar apenas em issues críticas, troque para
	`high`.

**Diagrama da arquitetura da pipeline**:

```mermaid
flowchart TD
	PR_PUSH[Push / Pull Request (main)] -->|dispara| Security[CodeQL<br/>(security scan)]
	PR_PUSH --> Test[Lint + Tests]
	Security -->|se OK| Deploy[Deploy to Stage]
	Test -->|se OK| Deploy
	Security -->|se falhar| Alert[Alerta de Vulnerabilidade]
	style Security fill:#ffe680,stroke:#333,stroke-width:1px
	style Test fill:#e6f7ff,stroke:#333,stroke-width:1px
	style Deploy fill:#e6ffe6,stroke:#333,stroke-width:1px
	style Alert fill:#ffd6d6,stroke:#900,stroke-width:1px
```

**Explicação dos estágios (didático)**:
- **Security (CodeQL)**: utiliza a Action oficial `github/codeql-action` para
	analisar o código em busca de vulnerabilidades. A entrada `fail-on` determina a
	severidade mínima que fará a pipeline falhar (ex.: `medium`). Se falhar, o
	job termina com erro e o deploy NÃO é executado.
- **Lint and Test**: instala dependências (se houver `requirements.txt`),
	instala ferramentas de desenvolvimento (`flake8`, `pytest`) e executa lint e
	testes unitários. Erros aqui também fazem a pipeline falhar.
- **Deploy to Stage**: exemplo educativo; só roda se os dois jobs anteriores
	forem bem-sucedidos. No exemplo este passo apenas cria um artefato e imprime
	instruções. Substitua por uma action de deploy real (SCP, rsync, S3, container
push, etc.) e use secrets para credenciais.

No exemplo implementado neste repositório, o passo de deploy usa a action
`appleboy/scp-action` para copiar o conteúdo de `build/` para o servidor de
stage via SCP. Os secrets necessários são listados acima (`STAGE_HOST`,
`STAGE_USER`, `STAGE_KEY`, `STAGE_TARGET`).

Como adicionar os secrets no GitHub:
1. No GitHub, abra `Settings` do repositório.
2. Vá em `Secrets and variables` → `Actions` → `New repository secret`.
3. Adicione `STAGE_HOST`, `STAGE_USER`, `STAGE_KEY` (conteúdo da chave privada
   em formato PEM) e `STAGE_TARGET`.


**Notas didáticas / Boas práticas**:
- Mantenha a análise de segurança sempre antes do deploy para evitar expor
	vulnerabilidades.
- Em projetos reais, adicione etapas de build/packaging e verificação de
	dependências (ex.: safety, pip-audit).
- Configure regras de branch protection no GitHub para bloquear merges em
	`main` caso a pipeline falhe.

**Alterando o nível de falha do CodeQL**:
- `fail-on: medium` — falha em vulnerabilidades *medium* e acima.
- `fail-on: high` — falha apenas em vulnerabilidades *high* e acima.

**Execução local / Testes**:
- A workflow roda no GitHub Actions. Para testar localmente, você pode usar o
	`act` (terceiro) mas nem todas as actions (especialmente CodeQL) funcionarão
	localmente de forma idêntica.

Se quiser, posso também:
- Gerar um `requirements.txt` mínimo com `pytest`/`flake8` para facilitar os
	testes em sala de aula.
- Ajustar o passo de deploy para um provedor específico (Heroku, Azure, SSH).

---
Arquivo da workflow: `/.github/workflows/ci-cd-python.yml`
