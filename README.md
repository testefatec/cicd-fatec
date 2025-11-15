# cicd-fatec

Este repositório contém um exemplo didático de pipeline CI/CD para projetos Python
com validação de segurança usando CodeQL (GitHub Advanced Security). O objetivo é
fornecer um pipeline curto, comentado e fácil de entender para uso em sala de aula.

**Arquivos principais**:
- `/.github/workflows/ci-cd-python.yml`: workflow do GitHub Actions com CodeQL,
	lint/tests e um passo de deploy para *stage* (placeholder).

**Visão rápida**:
- Ao enviar um push ou abrir uma pull request para `main`, a workflow dispara.
- O CodeQL roda e gera alertas de segurança (visíveis em `Security` → `Code scanning alerts`).
- Os alertas podem ser integrados com regras de branch protection para bloquear merges.
- Se CodeQL, testes/lint e demais verificações passarem, o job de *deploy-stage* é executado.

**Como usar (rápido)**:
1. Abra o repositório no GitHub.
2. Habilite o GitHub Advanced Security (Code Scanning) no repositório (se disponível).
3. Ajuste `/.github/workflows/ci-cd-python.yml` conforme sua infra de deploy real.

**Configurar secrets para deploy (exemplo)**:
- `STAGE_HOST`: host do servidor de stage
- `STAGE_USER`: usuário SSH
- `STAGE_KEY`: chave privada SSH (considere usar GitHub Encrypted Secrets)
 - `STAGE_TARGET`: diretório remoto onde os arquivos serão copiados (ex.: `/var/www/stage-app/`)
 - `STAGE_TARGET`: diretório remoto onde os arquivos seriam copiados (apenas se
	 usar SCP). NÃO é necessário quando você usa o `Environment` do GitHub.

**Onde editar a regra de falha do CodeQL**:
- A partir da versão 3 da ação CodeQL, o parâmetro `fail-on` foi removido.
- Em vez disso, as vulnerabilidades são reportadas como **Code scanning alerts** no GitHub.
- Para **bloquear merges** automaticamente quando há vulnerabilidades:
  1. Vá em `Settings` → `Branches` → `Add rule` para a branch `main`.
  2. Em `Require status checks to pass before merging`, ative `Code scanning — CodeQL`.
  3. Selecione o nível de severidade desejado (medium, high, critical).

Desta forma, a pipeline não "falha" diretamente, mas o GitHub bloqueia o merge se houver alertas.

**Diagrama da arquitetura da pipeline**: (removido a pedido do professor)

**Explicação dos estágios (didático)**:
- **Security (CodeQL)**: utiliza a Action oficial `github/codeql-action` para
	analisar o código em busca de vulnerabilidades. Os alertas são reportados em
	`Security` → `Code scanning alerts`. A categoria é `python-security` para
	análise específica de Python. Permissões (`security-events: write`) são
	necessárias para que o CodeQL faça upload dos resultados.
- **Lint and Test**: instala dependências (se houver `requirements.txt`),
	instala ferramentas de desenvolvimento (`flake8`, `pytest`) e executa lint e
	testes unitários. Erros aqui fazem a pipeline falhar.
- **Deploy to Stage**: só roda se os dois jobs anteriores forem bem-sucedidos.
	Este passo cria um artefato e faz upload para o Environment `stage`. Substitua
	por uma action de deploy real (SCP, rsync, S3, etc.) conforme sua necessidade.

Este repositório usa o recurso **Environment** do GitHub para o estágio `stage`.
Isso significa que não é necessário um servidor externo — o job de deploy
associa a execução ao Environment `stage` e faz o upload do artefato como
evidência do deploy.

Como criar o Environment `stage` no GitHub e adicionar secrets específicos:
1. No GitHub, abra `Settings` do repositório.
2. Vá em `Environments` → `New environment` e crie o environment com nome
	`stage`.
3. Dentro do Environment `stage`, adicione *Environment secrets* se desejar
	(ex.: variáveis de configuração para o ambiente). Esses secrets ficam
	restritos ao environment e podem exigir aprovações antes de permitir o
	deploy.

Se você quiser que o deploy copie arquivos para um servidor real, ainda é
possível: ajuste a workflow para usar SCP/rsync/S3 e mantenha os secrets no
Environment (ou em repository secrets), conforme sua preferência.


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
