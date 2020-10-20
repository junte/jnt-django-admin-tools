make_messages:
	@./manage.py makemessages -l de -l fr -l en -l it -l es --no-location

pre_commit:
	@ pre-commit

pre_commit_install:
	@ pre-commit install && pre-commit install --hook-type commit-msg

pre_commit_update:
	@ pre-commit autoupdate
