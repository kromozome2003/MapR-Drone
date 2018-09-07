# MapR-Drone
Draft under construction, don't clone/fork yet

## Setup your cluster/sandbox
Assuming your MapR cluster/sandbox is up & running w/IP 192.168.56.101 and you have a valid license for streams
Create sample stream for this demo
```
maprcli stream create -path /demos/drone/drone1 -produceperm p -consumeperm p -topicperm p -copyperm p -adminperm p
maprcli stream topic create -path /demos/drone/drone1 -topic frames
```

## Setup MapR PACC
### Retrieve the project
```
git clone https://github.com/kromozome2003/MapR-Drone.git
cd MapR-Drone
```
### Retrieve & Run the MapR setup script
```
wget http://package.mapr.com/releases/installer/mapr-setup.sh
chmod +x mapr-setup.sh
./mapr-setup.sh docker client
```
* Respond to the questions as is :
* Image OS class: ubuntu16
* Docker FROM base image name:tag: ubuntu:16.04
* MapR core version: 6.0.1
* MapR MEP version: 5.0.0
* Install Hadoop YARN client: y
* Add POSIX (FUSE) client to container: y
* Add HBase client to container: n
* Add Hive client to container: n
* Add Pig client to container: n
* Add Spark client to container: n
* Add Streams clients to container: y
* MapR client image tag name:  maprtech/pacc:6.0.1_5.0.0_ubuntu16_yarn_fuse_streams
* Container network mode:  bridge
* Container memory: 0
### Build the drone-client image (based on MapR PACC)
```
docker build -t drone-client Containers/drone-client/
```
### Edit the MapR script to setup your cluster
```
vi Containers/drone-client/docker_images/client/mapr-docker-client.sh
```
Assuming your MapR cluster/sandbox is up & running with IP 182.168.56.101 (VBox default host-only)
* MAPR_CLUSTER=demo.mapr.com
* MAPR_CLDB_HOSTS=192.168.56.101:7222
* MAPR_MOUNT_PATH=/mapr
* MAPR_CONTAINER_USER=mapr
* MAPR_CONTAINER_UID=2000
* MAPR_CONTAINER_PASSWORD=mapr
* LAST LINE —> replace  maprtech/pacc:6.0.1_5.0.0_ubuntu16_yarn_fuse_streams by  test1:latest
### Run the container
```
chmod +x Containers/drone-client/docker_images/client/mapr-docker-client.sh
cd Containers/drone-client
./run_container.sh
```
### Once in the container shell, run the producer/consumer/drone-stream
```
export LD_LIBRARY_PATH=/opt/mapr/lib:/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server
python producer-flask.py /demos/drone/drone1:frames
python stream_drone_video.py -s /demos/drone/drone1 -t frames
python consumer-flask.py /demos/drone/drone1:frames
```
## Visit the web page to see live streaming from the Drone
[http://localhost:5000/](http://localhost:5000/)
