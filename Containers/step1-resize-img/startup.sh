#!/bin/bash
cd /home/mapr
export LD_LIBRARY_PATH=/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server
nohup python /home/mapr/consumer-flask.py /demos/drone/drone1:resized > /home/mapr/resize.out &
nohup python /home/mapr/resize-img.py /demos/drone/drone1:frames /demos/drone/drone1:resized 418 >> /home/mapr/resize.out &
tail -f /home/mapr/resize.out
