# Executa core.py
run:
	python src/producer_consumer_sync/core.py

# Instala as dependências necessárias para o desenvolvimento
install:
	pip install -r requirements/dev.txt

# Executa os testes unitários
test:
	pytest tests/ -v

# Executa testes em modo watch para prática de TDD
tdd:
	ptw -v

tdd-fail:
	ptw -v -- --last-failed

tdd-debug:
	ptw -v --pdb

# Verifica a qualidade do código
lint:
	# Verifica a sintaxe e a formatação do código
	flake8 src/
	# Verifica a formatação do código
	black --check src/ tests/
	# Verifica a tipagem do código
	mypy src/ tests/

# Formata o código
format:
	# Formata o código para seguir as convenções de estilo
	black src/ tests/
	# Organiza as importações
	isort src/ tests/

# Gera um relatório de cobertura de código
coverage:
	# Executa os testes e gera um relatório de cobertura
	pytest --cov=producer_consumer_sync --cov-report=html

all: install format lint coverage

