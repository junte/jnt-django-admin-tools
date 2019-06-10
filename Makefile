flake8:
	@flake8 src

check_quality: flake8

build:
	poetry build

publish:
	poetry publish

release: build publish
