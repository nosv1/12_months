uv run mypy ./ --check-untyped-defs
read -rp "Enter to continue..."
uv run pytest
read -rp "Enter to continue..."
uv run telemetry ./data/sample_telemetry.csv output