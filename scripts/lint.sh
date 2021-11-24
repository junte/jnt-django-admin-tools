#!/usr/bin/env sh

set -o errexit
set -o nounset

run_checkers() {
  black --check .

#  mypy .

  flake8 .

#  xenon --max-absolute A --max-modules A --max-average A .

  # Checking `pyproject.toml` file contents:
  poetry check

  # Checking dependencies status:
  pip check

  # Checking if all the dependencies are secure and do not have any
  # known vulnerabilities:
#  safety check --bare --full-report

  # po files
#  polint -i location,unsorted locale
}

run_checkers
