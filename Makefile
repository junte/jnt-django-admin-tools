lint:
	black --check .
#  mypy .
	flake8 .
#  xenon --max-absolute A --max-modules A --max-average A .
	poetry check
	pip check

build:
	@poetry build

publish:
	@poetry publish

release: build publish

pre-commit:
	@pre-commit

pre-commit-install:
	@pre-commit install
	@pre-commit install --hook-type commit-msg
