mypy:
    pdm run mypy src/ tests

ruff:
    pdm run ruff src/ tests

fmt:
    pdm run ruff format --check src/ tests

lint: mypy ruff fmt

test *args="":
    pdm run pytest {{args}}