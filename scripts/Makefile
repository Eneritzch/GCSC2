# Atajos para tareas comunes del proyecto.
# Uso: make <objetivo>   (por ejemplo: make run)

.PHONY: install migrate run seed test lint clean

install:      ## Instala dependencias de desarrollo
	pip install -r requirements-dev.txt

migrate:      ## Aplica migraciones de la base de datos
	python manage.py migrate

run:          ## Levanta el servidor de desarrollo
	python manage.py runserver

seed:         ## Carga datos de prueba
	python manage.py seed_datos

test:         ## Ejecuta los tests
	python manage.py test

lint:         ## Revisa el estilo del codigo con flake8
	flake8 .

clean:        ## Elimina archivos temporales de Python
	find . -type d -name __pycache__ -exec rm -rf {} +
