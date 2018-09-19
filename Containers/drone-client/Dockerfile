FROM maprtech/pacc:6.0.1_5.0.0_ubuntu16_yarn_streams

# System
RUN sudo apt-get update -y
RUN sudo apt-get install -y vim
RUN sudo apt-get install -y locate

# Python2.7 + Libs
RUN sudo apt-get install -y python2.7 python-pip
RUN sudo pip install --upgrade pip
RUN sudo apt-get install -y python-dev pkg-config
RUN sudo apt-get install -y libavformat-dev
RUN sudo apt-get install -y libavcodec-dev
RUN sudo apt-get install -y libavdevice-dev
RUN sudo apt-get install -y libavutil-dev
RUN sudo apt-get install -y libswscale-dev
RUN sudo apt-get install -y libavresample-dev
RUN sudo apt-get install -y libavfilter-dev
RUN sudo pip install av
RUN sudo pip install requests
RUN sudo apt-get install -y python-opencv
RUN sudo pip install image
RUN sudo apt-get install -y python-numpy

# Python lib for Ryze (DJI) Tello drone
RUN sudo pip install tellopy
EXPOSE 9000/udp
EXPOSE 6038/udp

# MapR-ES setup
RUN export LD_LIBRARY_PATH=/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server
RUN sudo pip install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" mapr-streams-python

# Copy scripts
COPY stream_drone_video.py /home/mapr/
COPY video.mp4 /home/mapr/
COPY video-producer.py /home/mapr/
COPY startup.sh /home/mapr/
RUN sudo chmod +x /home/mapr/startup.sh
CMD /home/mapr/startup.sh
