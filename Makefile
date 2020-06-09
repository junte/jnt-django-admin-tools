check_quality:
	@./scripts/quality.sh

build:
	poetry build

publish:
	poetry publish

release: build publish
