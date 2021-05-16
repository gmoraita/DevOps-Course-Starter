#!/bin/sh
echo "Build the TODO list"
docker build --target production --tag $DOCKER_USER/todo-app:$TRAVIS_COMMIT .
echo "Push the TODO list to Docker Hub"
echo $DOCKER_PWD | docker login --username $DOCKER_USER --password-stdin
docker push $DOCKER_USER/todo-app:$TRAVIS_COMMIT
docker pull $DOCKER_USER/todo-app:$TRAVIS_COMMIT
docker tag $DOCKER_USER/todo-app:$TRAVIS_COMMIT registry.heroku.com/georgestodoapp/web
HEROKU_API_KEY=$HEROKU_API_KEY heroku container:login
docker push registry.heroku.com/georgestodoapp/web
HEROKU_API_KEY=$HEROKU_API_KEY heroku container:release web -a georgestodoapp