# Manage requirements
pip-install:
	pip install --upgrade pip
	pip install -r requirements.txt

# Manage CI tools
mypy:
	mypy --strict --config-file=mypy.ini --exclude manage.py .

ruff:
	ruff check .

test:
	python manage.py test

check: mypy ruff test

clean:
	ruff check --fix .
	ruff format .

# Running the project
server:
	python manage.py migrate && python manage.py runserver

checkmigrations:
	python manage.py makemigrations --check --no-input --dry-run

migrations:
	python manage.py makemigrations && python manage.py migrate
