#!/bin/bash
cd /home/mapr
export LD_LIBRARY_PATH=/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server
#nohup python producer-flask.py /demos/drone/drone1:frames &
#python stream_drone_video.py -s /demos/drone/drone1 -t frames
python /home/mapr/consumer-flask.py /demos/drone/drone1:frames > /home/mapr/flask.out
