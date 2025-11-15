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
 - `STAGE_TARGET`: diretório remoto onde os arquivos seriam copiados (apenas se
	 usar SCP). NÃO é necessário quando você usa o `Environment` do GitHub.

**Onde editar a regra de falha do CodeQL**:
- No arquivo `/.github/workflows/ci-cd-python.yml`, a opção `fail-on` está
	configurada como `medium`. Para falhar apenas em issues críticas, troque para
	`high`.

**Diagrama da arquitetura da pipeline**: (removido a pedido do professor)

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
