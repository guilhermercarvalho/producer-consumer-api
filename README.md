# Produtor e Consumidor

- [] que problema é esse? **refatorar reascunho inicial**

## Problema de Sincronização

- [ ] o que é um problema de sincronização?

## Branches

- `main`: principal
- `feat/xpto`: adiciona funcionalidade

# Stack

- [x] como funciona o `requirements` do `pip`?
    - Arquivos que listam dependências do projeto (pacotes Python necessários)
        - prod.txt: Dependências de produção (ex: numpy, requests)
        - dev.txt: Dependências de desenvolvimento (testes, formatação, etc.)
- [x] em `src` o que é um `__init__.py` e `core.py`
    - \_\_init\_\_.py: Transforma a pasta em um pacote Python (permite imports como from <MYPROJECT> import ...)
    - core.py: Módulo principal com a lógica central do projeto (ex: funções/classes principais)
- [x] em `tests` o que é um `__init__.py` e `test_core.py`
    - \_\_init\_\_.py: Similar ao do src, indica que testes são parte de um pacote
    - test_core.py: Arquivo de testes para core.py (usa pytest/unittest)
- [x] quais as configurações possíveis de `flake8`?
    - Linter que verifica estilo (PEP8). Exemplo de configuração (.flake8 ou pyproject.toml)
- [ ] quais arquivos estão sendo ignorados em `.gitignore`?
- [x] como funciona um `Makefile`?
    - Automatiza comandos via terminal, exemplo, `make lint`, `make test`
- [x] o que é um `pyproject.toml`?
    - Substitui setup.py em projetos modernos. Dependências
        - Build system (ex: poetry, setuptools)
        - Ferramentas (Black, Flake8)
- [x] como funciona o `pytest.ini`?
    - Configurações do Pytest
- [x] como funciona o `github/workflows` e que a **action** `tests.yml` faz?
    - Automatiza CI/CD. A action tests.yml executa testes em cada push/pull request
        - Instala dependências
        - Roda testes e gera relatório de coverage
- [x] o que são:
    - **flake8**	Verifica estilo PEP8
    - **black**	Formata código automaticamente
    - **mypy**	Checagem estática de tipos
    - **pytest**	Framework de testes (mais moderno que unittest)
    - **virtualenv**	Isola ambientes Python
    - **pylint**	Analisa código para encontrar erros e más práticas
    - **bandit**	Verifica vulnerabilidades de segurança
    - **pipenv**	Gerenciador de dependências + virtualenv
    - **autopep8**	Formata código para PEP8
    - **yapf**	Formatação alternativa ao Black
    - **pydocstyle**	Verifica docstrings
    - **pycodestyle**	Antigo nome do pep8 (similar ao flake8)
- [x] como funciona as extensões do vscode:
    - **ms-python.python** Suporte básico para Python (execução, debug)
        - **ms-python.debugpy**
    - **ms-python.vscode-pylance** Suporte para edição de workflows do GitHub
    - **ms-python.black-formatter** Formata código com Black automaticamente
    - **ms-python.autopep8**
    - **streetsidesoftware.code-spell-checker** Verifica ortografia em código/comentários
        - **streetsidesoftware.code-spell-checker-portuguese-brazilian**
    - **github.vscode-github-actions** Suporte para edição de workflows do GitHub

## Fluxo de Trabalho Típico

1. Desenvolver em `src/`
2. Testar com `pytest tests/`
3. Formatar com `black src/ tests/`
4. Verificar estilo com `flake8 src/`
5. Commitar com Git
6. CI/CD via GitHub Actions valida automaticamente
