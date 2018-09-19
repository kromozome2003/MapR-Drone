#!/bin/bash
#docker run --rm -it -p 5001:5001/tcp $MAPR_DOCKER_ARGS step1-resize-img:latest "$@"
cd /home/mapr
export LD_LIBRARY_PATH=/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server
python /home/mapr/resize-img.py /demos/drone/drone1:frames /demos/drone/drone1:resized 448
