install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

lint:
	@echo "Running code quality checks..."
	@poetry run ruff check . && echo "All checks passed!" || exit 1

fix:
	poetry run ruff check . --fix