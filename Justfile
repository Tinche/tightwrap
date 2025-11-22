mypy:
    uv run mypy src/ tests

ruff:
    uv run ruff check src/ tests

fmt:
    uv run ruff format --check src/ tests

lint: mypy ruff fmt

test *args="":
    uv run pytest {{args}}

sync:
    uv sync --all-groups
