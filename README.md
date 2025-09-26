🧊  **Code Freeze Checker com GitLab**

Este projeto implementa um sistema de controle de deploys em períodos de congelamento (freezing dates) integrado ao GitLab.

Ele utiliza um arquivo de configuração YAML (config.yml) para definir:

Usuários autorizados a realizar deploys mesmo durante o congelamento.

Períodos de bloqueio (como Black Friday, Carnaval, fim de ano etc.), durante os quais os deploys devem ser restritos.

Se um usuário que não faz parte do grupo liberado tentar realizar uma ação durante uma data de bloqueio, o processo é encerrado com erro.


⚙️  **Como Funciona**

O script main.py:

Carrega o arquivo config.yml.

Verifica se o usuário (GITLAB_USER_LOGIN) está no grupo de exceção (glass_breaker_group).

Caso contrário, checa se a data atual está dentro de algum período de bloqueio.

Se estiver dentro do período → bloqueia (exit code 1).

Se não estiver → permite a execução (exit code 0).

O docker-compose.yml:

Sobe um ambiente com GitLab CE, Docker-in-Docker (DinD) e GitLab Runner para CI/CD.

Esse setup permite integrar o script nos pipelines do GitLab.

O config.yml:

Define os usuários liberados e os períodos de congelamento.

📜 Exemplo de config.yml
---
glass_breaker_group:
  - vitor
  - root

freezing_dates:
  End of the Year:
    from: 2025-12-24
    to: 2026-01-03
  Carnival:
    from: 2025-02-28
    to: 2025-03-05
  Black Friday:
    from: 2025-11-20
    to: 2025-11-30
  Test:
    from: 2025-09-23
    to: 2025-09-29

🚀 **Executando o Projeto**
1. Subir o ambiente com GitLab + Runner
docker-compose up -d

2. Rodar o script manualmente
export GITLAB_USER_LOGIN=vitor
python3 main.py

3. Integração no GitLab CI/CD

Adicione no .gitlab-ci.yml:

stages:
  - check
  - deploy

freeze-check:
  stage: check
  script:
    - python3 main.py

deploy:
  stage: deploy
  script:
    - echo "Deploy liberado!"
  needs: ["freeze-check"]

🛠️ Requisitos

Python 3.8+

Bibliotecas Python:

pyyaml

Docker e Docker Compose para rodar o ambiente GitLab

Instale as dependências:

pip install pyyaml

📌 Fluxo de Decisão

Se GITLAB_USER_LOGIN ∈ glass_breaker_group → ✅ Deploy permitido.

Se hoje ∈ algum freezing_dates → ❌ Deploy bloqueado.

Caso contrário → ✅ Deploy permitido.

📊 Exemplo de Logs
2025-09-25 23:41:12 - root - INFO - Validating period Test that goes from 2025-09-23 to 2025-09-29
2025-09-25 23:41:12 - root - WARNING - The date current falls under Test, blocked due to blockout period

👤 Autor

Projeto desenvolvido por Vitor Bretz.