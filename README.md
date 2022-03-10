# tlu_management_docker

# build:

docker-compose build

# run command in docker:

docker-compose run --rm app sh -c "django-admin startproject app ."
docker-compose run --rm app sh -c "python manage.py startapp core"
docker-compose run --rm app sh -c "python manage.py makemigrations"

# start docker

docker-compose up
