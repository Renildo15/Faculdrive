# Formata o código usando Black e Isort
format:
	black .
	isort .

# Cria e aplica as migrações
migrate:
	python manage.py makemigrations
	python manage.py migrate

# Executa o servidor de desenvolvimento
server:
	python manage.py runserver 192.168.1.13:8000

# Abre o shell do Django
shell:
	python manage.py shell

# Inicializa o superusuário (admin)
admin:
	python manage.py initadmin

# Aplica migrações do django-celery-beat
celery-beat:
	python manage.py migrate django_celery_beat

# Executa o Celery Beat
celery-beat-run:
	celery -A buslist beat --loglevel=info

# Executa o Celery Worker
celery-run:
	celery -A buslist worker --loglevel=info

# Executa o flower
flower-run:
	celery -A buslist flower

# Inicia o servidor Redis
redis:
	redis-server

# Gera o arquivo requirements.txt
add-dependencies:
	pip freeze > requirements.txt

# Instala as dependências do projeto
dependencies:
	pip install -r requirements.txt

# Inicia o banco de dados com Docker Compose
db:
	docker compose up db

# Executa os testes com unittest
test_unittest:
	python manage.py test

# Executa os testes com pytest
test_pytest:
	pytest

# Executa os testes com pytest e gera relatório de cobertura
coverage:
	coverage run -m pytest
	coverage report
	coverage html