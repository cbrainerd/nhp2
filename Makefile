pylint:
	pylint -E wgups

pytest:
	pytest -v wgups/tests

black:
	black .
