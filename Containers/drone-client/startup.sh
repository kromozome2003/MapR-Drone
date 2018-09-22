#!/bin/bash
#docker run --rm -it -p 6038:6038/udp -p 9000:9000/udp $MAPR_DOCKER_ARGS drone-client:latest "$@"
cd /home/mapr
export LD_LIBRARY_PATH=/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server
python video-producer.py /demos/drone/drone1:frames
#python stream_drone_video.py -s /demos/drone/drone1 -t frames -d 30
