#!/bin/bash
#docker run --rm -it -p 6038:6038/udp -p 9000:9000/udp $MAPR_DOCKER_ARGS drone-client:latest "$@"
cd /home/mapr
export LD_LIBRARY_PATH=/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server
python /home/mapr/consumer-flask.py /demos/drone/drone1:frames /demos/drone/drone1:resized /demos/drone/drone1:analyzed
#gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:5000 consumer-flask:app
