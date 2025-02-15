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

## Ajustes necessários

Aqui está uma lista de tarefas resumida com as refatorações necessárias para melhorar a API Flask, seguindo princípios SOLID, Clean Architecture e boas práticas de design:

---

### **1. Estrutura do Projeto**
- [ ] Criar a estrutura de pastas:
  ```
  src/
  ├── api/
  │   ├── controllers/
  │   ├── errors/
  │   ├── routes.py
  │   └── app.py
  ├── core/
  │   ├── services/
  │   ├── repositories/
  │   └── domain/
  └── main.py
  ```

---

### **2. Camada de Domínio**
- [ ] Criar modelos de dados em `core/domain/models.py`:
  - Definir `ProcessStatus` como um dataclass.
  - Criar exceção `ProcessNotFoundError`.

---

### **3. Camada de Repositório**
- [ ] Implementar `ProcessRepository` em `core/repositories/process_repository.py`:
  - Criar métodos para gerenciar processos (`create_process`, `get_process`, `stop_process`).
  - Usar `multiprocessing.Manager` para armazenar processos.

---

### **4. Camada de Serviço**
- [ ] Implementar `ProcessService` em `core/services/process_service.py`:
  - Injetar `ProcessRepository` como dependência.
  - Implementar métodos para iniciar, verificar status e parar processos.

---

### **5. Camada de API**
- [ ] Criar `ProcessController` em `api/controllers/process_controller.py`:
  - Injetar `ProcessService` como dependência.
  - Implementar métodos para os endpoints (`start`, `get_status`, `stop`).

---

### **6. Tratamento de Erros**
- [ ] Criar handlers de erro em `api/errors/handlers.py`:
  - Implementar `handle_process_not_found` para erros de processo não encontrado.
  - Implementar `handle_generic_error` para erros genéricos.

---

### **7. Configuração das Rotas**
- [ ] Configurar rotas em `api/routes.py`:
  - Definir rotas para `/start`, `/status/<process_id>` e `/stop/<process_id>`.
  - Registrar handlers de erro.

---

### **8. Aplicação Flask**
- [ ] Criar a aplicação Flask em `api/app.py`:
  - Implementar `create_app` para configurar a aplicação.
  - Chamar `setup_routes` para configurar as rotas.

---

### **9. Ponto de Entrada**
- [ ] Criar `main.py` para iniciar a aplicação:
  - Importar e executar `create_app`.

---

### **10. Testes**
- [ ] Criar testes unitários para cada camada:
  - Testar `ProcessRepository`.
  - Testar `ProcessService`.
  - Testar `ProcessController`.
  - Testar handlers de erro.

---

### **11. Validação de Entrada**
- [ ] Adicionar validação de dados de entrada:
  - Validar `buffer_type` no endpoint `/start`.
  - Validar `process_id` nos endpoints `/status` e `/stop`.

---

### **12. Documentação da API**
- [ ] Adicionar suporte a OpenAPI/Swagger:
  - Usar `flask-swagger-ui` para documentação automática.
  - Definir esquemas para os endpoints.

---

### **13. Logging**
- [ ] Implementar logging centralizado:
  - Registrar eventos importantes (ex: início/parada de processos).
  - Logar erros e exceções.

---

### **14. Autenticação/Autorização**
- [ ] Adicionar autenticação:
  - Implementar JWT ou OAuth2.
  - Proteger endpoints sensíveis.

---

### **15. CI/CD**
- [ ] Configurar CI/CD:
  - Adicionar testes automatizados.
  - Configurar deploy automático.

---

### **Resumo das Tarefas**
1. Estruturar o projeto.
2. Implementar camada de domínio.
3. Implementar camada de repositório.
4. Implementar camada de serviço.
5. Implementar camada de API.
6. Configurar tratamento de erros.
7. Configurar rotas.
8. Criar aplicação Flask.
9. Criar ponto de entrada.
10. Escrever testes unitários.
11. Adicionar validação de entrada.
12. Documentar a API.
13. Implementar logging.
14. Adicionar autenticação.
15. Configurar CI/CD.

---

Seguindo essa lista, você terá uma API Flask bem estruturada, modular e pronta para escalar.
