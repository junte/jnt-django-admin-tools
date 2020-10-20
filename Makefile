check_quality:
	@./scripts/quality.sh

build:
	poetry build

publish:
	poetry publish

release: build publish

pre_commit:
	@ pre-commit

pre_commit_install:
	@ pre-commit install && pre-commit install --hook-type commit-msg

pre_commit_update:
	@ pre-commit autoupdate
