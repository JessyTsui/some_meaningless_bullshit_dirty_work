TAG=${1:-latest}

docker run --rm -it \
    -p 5000:5000 \
    -v /etc/localtime:/etc/localtime:ro \
    -v "$PWD/src":"/opt/pku-embl" \
     pku-ece-cv:$TAG \
     conda run --no-capture-output --name pku-embl python3 app.py -d -vv