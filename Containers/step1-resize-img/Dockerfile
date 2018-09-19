FROM maprtech/pacc:6.0.1_5.0.0_ubuntu16_yarn_streams

# System
RUN sudo apt-get update -y
RUN sudo apt-get install -y vim
RUN sudo apt-get install -y locate

# Python2.7 + Libs
RUN sudo apt-get install -y python2.7 python-pip
RUN sudo pip install --upgrade pip
RUN sudo apt-get install -y python-dev pkg-config
RUN sudo pip install image

# MapR-ES setup
RUN export LD_LIBRARY_PATH=/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server
RUN sudo pip install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" mapr-streams-python

# Copy scripts
COPY resize-img.py /home/mapr/
COPY startup.sh /home/mapr/
RUN sudo chmod +x /home/mapr/startup.sh
CMD /home/mapr/startup.sh
