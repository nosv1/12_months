echo 'ruff...'
uv run ruff check --fix

echo 'mypy...'
uv run mypy ./ --check-untyped-defs
read -rp "Enter to continue..."

echo 'pytest...'
uv run pytest
read -rp "Enter to continue..."

echo 'telemetry...'
uv run telemetry ./data/sample_telemetry.csv output