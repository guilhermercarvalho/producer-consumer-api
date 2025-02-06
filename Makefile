install:
    pip install -r requirements/dev.txt

test:
    pytest tests/ -v

lint:
    flake8 src/
    black --check src/ tests/
    mypy src/

format:
    black src/ tests/
    isort src/ tests/

coverage:
    pytest --cov=producer-consumer-sync --cov-report=html
