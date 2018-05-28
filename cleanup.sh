docker volume prune
docker network prune
docker container prune
docker image prune
docker images --no-trunc | grep '<none>' | awk '{ print $3 }' | xargs -r docker rmi
docker stack rm sassapp
docker stack rm sassbank


