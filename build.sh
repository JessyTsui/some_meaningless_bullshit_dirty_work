TAG=${1:-latest}

docker build -t pku-embl:$TAG  -f ./docker/Dockerfile .